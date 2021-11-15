import time
from subprocess import PIPE, Popen, TimeoutExpired

import psutil

from ...error import ShellError, SSConfigError
from ...utils import get_env, get_logger

logger = get_logger(__name__)


from smartsim.worker import tasks

def execute_cmd(cmd_list, shell=False, cwd=None, env=None, proc_input="", timeout=None):
    task = tasks.execute_command(cmd_list, shell, cwd, env, proc_input, timeout)
    result = task.wait(propagate=True)
    return result

def execute_async_cmd(cmd_list, cwd, env=None, out=PIPE, err=PIPE):
    """Execute an asynchronous command

    This function executes an asynchronous command and returns a
    popen subprocess object wrapped with psutil.

    :param cmd_list: list of command with arguments
    :type cmd_list: list of str
    :param cwd: current working directory
    :type cwd: str
    :param env: environment variables to set
    :type env: dict
    :return: the subprocess object
    :rtype: psutil.Popen
    """
    global verbose_shell
    if verbose_shell:
        logger.debug(f"Executing command: {' '.join(cmd_list)}")

    try:
        popen_obj = psutil.Popen(
            cmd_list, cwd=cwd, stdout=out, stderr=err, env=env, close_fds=True
        )
        time.sleep(0.2)
        popen_obj.poll()
        if not popen_obj.is_running() and popen_obj.returncode != 0:
            output, error = popen_obj.communicate()
            err_msg = ""
            if output:
                err_msg += output.decode("utf-8") + " "
            if error:
                err_msg += error.decode("utf-8")
            raise ShellError("Command failed immediately", err_msg, cmd_list)
    except OSError as e:
        raise ShellError("Failed to run command", e, cmd_list) from None
    return popen_obj
