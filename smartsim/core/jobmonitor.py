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

import itertools
import time
from threading import Thread
import threading
from ..config import CONFIG
from ..constants import LOCAL_JM_INTERVAL, TERMINAL_STATUSES
from ..database import Orchestrator
from ..database.orchestrator import get_ip_from_host
from ..entity import DBNode
from ..error import SmartSimError, SSConfigError, SSUnsupportedError
from ..launcher import LocalLauncher
from .backend.crud import job
from ..utils import get_logger
from .job import Job
from ..launcher import (
    CobaltLauncher,
    LocalLauncher,
    LSFLauncher,
    PBSLauncher,
    SlurmLauncher,
)

# as multiple different threads can access the job manager
# we use a simple RLock to ensure that no outside thread is
# interrupting a transaction
JM_LOCK = threading.RLock()

logger = get_logger(__name__)

class JobMonitor:

    def __init__(self):
        self.actively_monitoring = False  # on/off flag
        self.launcher = None


    def run(self):
        logger.debug("Starting Job Manager")

        self.actively_monitoring = True
        while self.actively_monitoring:

            self._thread_sleep()
            jobs = self.check_jobs()  # update all job statuses at once
            for job in jobs:

                # if the job has errors then output the report
                # this should only output once
                if job.returncode is not None and job.status in TERMINAL_STATUSES:
                    if int(job.returncode) != 0:
                        logger.warning(job)
                        logger.warning(job.error_report())
                        self.move_to_completed(job)
                    else:
                        # job completed without error
                        logger.info(job)
                        self.move_to_completed(job)

            # if no more jobs left to actively monitor
            if not self():
                #self.actively_monitoring = False
                logger.debug("Sleeping, no jobs to monitor (not really)")


    def check_jobs(self):
        """Update all jobs in jobmanager

        Update all jobs returncode, status, error and output
        through one call to the launcher.

        """
        self._lock.acquire()
        try:
            jobs = self().values()
            job_name_map = dict([(job.name, job.ename) for job in jobs])

            # returns (job step name, StepInfo) tuples
            statuses = self._launcher.get_step_update(job_name_map.keys())
            for job_name, status in statuses:
                job = self[job_name_map[job_name]]
                # uses abstract step interface
                job.set_status(
                    status.status,
                    status.launcher_status,
                    status.returncode,
                    error=status.error,
                    output=status.output,
                )
        finally:
            self._lock.release()


    def init_launcher(self, launcher):
        """Initialize the controller with a specific type of launcher.

        SmartSim currently supports slurm, pbs(pro), cobalt, lsf,
        and local launching

        :param launcher: which launcher to initialize
        :type launcher: str
        :raises SSUnsupportedError: if a string is passed that is not
                                    a supported launcher
        :raises SSConfigError: if no launcher argument is provided.
        """
        launcher_map = {
            "slurm": SlurmLauncher,
            "pbs": PBSLauncher,
            "cobalt": CobaltLauncher,
            "lsf": LSFLauncher,
            "local": LocalLauncher
        }

        if launcher is not None:
            launcher = launcher.lower()
            if launcher in launcher_map:
                # create new instance of the launcher
                self.launcher = launcher_map[launcher]()
            else:
                raise SSUnsupportedError("Launcher type not supported: " + launcher)
        else:
            raise SSConfigError("Must provide a 'launcher' argument")


    def _thread_sleep(self):
        """Sleep the job manager for a specific constant
        set for the launcher type.
        """
        if isinstance(self._launcher, (LocalLauncher)):
            time.sleep(LOCAL_JM_INTERVAL)
        else:
            time.sleep(CONFIG.jm_interval)

