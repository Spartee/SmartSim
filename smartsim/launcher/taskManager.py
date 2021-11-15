# BSD 2-Clause License
#
# Copyright (c) 2021, Hewlett Packard Enterprise
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import os
import time
from subprocess import PIPE
from threading import RLock, Thread

import psutil

from smartsim.error.errors import SmartSimError

from ..constants import TM_INTERVAL
from .. import constants
from ..error import LauncherError
from ..utils import get_logger

from smartsim.worker import tasks

logger = get_logger(__name__)

try:
    level = os.environ["SMARTSIM_LOG_LEVEL"]
    verbose_tm = True if level == "developer" else False
except KeyError:
    verbose_tm = False


class TaskManager:
    """The Task Manager watches the subprocesses launched through
    the asyncronous shell interface. Each task is a wrapper
    around the Popen/Process instance.

    The Task Managers polls processes on smartsim.constants.TM_INTERVAL
    and detects job failure and completion. Upon termination, the
    task returncode, output, and error are added to the task history.

    When a launcher uses the task manager to start a task, the task
    is either managed (by a WLM) or unmanaged (meaning not managed by
    a WLM). In the latter case, the Task manager is responsible for the
    lifecycle of the process.
    """

    def __init__(self):
        """Initialize a task manager thread."""
        self.tasks = []

    def start_task(self, cmd_list, cwd, env=None, out=PIPE, err=PIPE):
        """Start a task managed by the TaskManager

        This is an "unmanaged" task, meaning it is NOT managed
        by a workload manager

        :param cmd_list: command to run
        :type cmd_list: list[str]
        :param cwd: current working directory
        :type cwd: str
        :param env: environment to launch with
        :type env: dict[str, str], optional
        :param out: output file, defaults to PIPE
        :type out: file, optional
        :param err: error file, defaults to PIPE
        :type err: file, optional
        :return: task id
        :rtype: int
        """
        if out == PIPE:
            task = tasks.execute_command.delay(cmd_list, cwd=cwd, env=env)
        else:
            task = tasks.execute_command_and_write.delay(cmd_list, cwd=cwd, env=env, out=out, error=err)
        if verbose_tm:
            logger.debug(f"Starting Task {task.id}")
        self.tasks.append(task)
        return task.id


    def start_and_wait(self, cmd_list, cwd, env=None, timeout=None):
        """Start a task not managed by the TaskManager

        This method is used by launchers to launch managed tasks
        meaning that they ARE managed by a WLM.

        This is primarily used for batch job launches

        :param cmd_list: command to run
        :type cmd_list: list[str]
        :param cwd: current working directory
        :type cwd: str
        :param env: environment to launch with
        :type env: dict[str, str], optional
        :param timeout: time to wait, defaults to None
        :type timeout: int, optional
        :return: returncode, output, and err
        :rtype: int, str, str
        """
        task = tasks.execute_command.delay(cmd_list, cwd=cwd, env=env, timeout=timeout)
        returncode, out, err = task.wait()
        if verbose_tm:
            logger.debug("Ran and waited on task")
        return returncode, out, err

    def remove_task(self, task_id):
        """Remove a task from the TaskManager

        :param task_id: id of the task to remove
        :type task_id: str
        """
        if verbose_tm:
            logger.debug(f"Removing Task {task_id}")
        task = self[task_id]
        if not task.ready():
            task.revoke(terminate=True, wait=True)

    def get_task_update(self, task_id):
        """Get the update of a task

        :param task_id: task id
        :type task_id: str
        :return: status, returncode, output, error
        :rtype: str, int, str, str
        """
        task = self[task_id]
        if not task.ready():
            return "Running", None, None, None

        if task.status == "FAILURE":
            failure = task.wait()
            raise SmartSimError("Shit got fucked up")
        elif task.status == "SUCCESS":
            result = task.wait()
            return "Completed", result[0], result[1], result[2]
        else:
            raise SmartSimError("Unknown task status")


    def __getitem__(self, task_id):
        for task in self.tasks:
            if task.id == task_id:
                return task
        raise KeyError

