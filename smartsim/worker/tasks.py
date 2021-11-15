
import logging
import time
import subprocess
from subprocess import PIPE, TimeoutExpired
import socket
#from ..error import SmartSimError, ShellError
#from smartsim.utils.log import get_logger
from pathlib import Path
import os
import psutil
import redis
from rediscluster import RedisCluster
from rediscluster.exceptions import ClusterDownError, RedisClusterException
from shutil import which


try:
    level = os.environ["SMARTSIM_LOG_LEVEL"]
    verbose_shell = bool(level == "developer")
except KeyError:
    verbose_shell = False

from celery import Celery
app = Celery(__name__, backend='redis://localhost', broker='redis://localhost')


def _execute_cmd(cmd_list, shell=False, cwd=None, env=None, proc_input="", timeout=None):
    """Execute a command locally

    :param cmd_list: list of command with arguments
    :type cmd_list: list of str
    :param shell: run in system shell, defaults to False
    :type shell: bool, optional
    :param cwd: current working directory, defaults to None
    :type cwd: str, optional
    :param env: environment to launcher process with,
                defaults to None (current env)
    :type env: dict, optional
    :param proc_input: input to the process, defaults to ""
    :type proc_input: str, optional
    :param timeout: timeout of the process, defaults to None
    :type timeout: int, optional
    :raises ShellError: if timeout of process was exceeded
    :raises ShellError: if child process raises an error
    :return: returncode, output, and error of the process
    :rtype: tuple of (int, str, str)
    """
    global verbose_shell

    if verbose_shell:
        source = "shell" if shell else "Popen"

    # spawning the subprocess and connecting to its output
    proc = psutil.Popen(
        cmd_list, stderr=PIPE, stdout=PIPE, stdin=PIPE, cwd=cwd, shell=shell, env=env
    )
    try:
        proc_input = proc_input.encode("utf-8")
        out, err = proc.communicate(input=proc_input, timeout=timeout)
    except TimeoutExpired as e:
        proc.kill()
        _, errs = proc.communicate()
        raise Exception(
            "Failed to execute command, timeout reached", e, cmd_list
        ) from None
    except OSError as e:
        raise Exception(
            "Exception while attempting to start a shell process", e, cmd_list
        ) from None

    # decoding the output and err and return as a string tuple
    return proc.returncode, out.decode("utf-8"), err.decode("utf-8")



def _execute_cmd_and_write(cmd_list, shell=False, cwd=None, env=None, proc_input="", timeout=None, output=None, error=None):
    """Execute a command locally

    :param cmd_list: list of command with arguments
    :type cmd_list: list of str
    :param shell: run in system shell, defaults to False
    :type shell: bool, optional
    :param cwd: current working directory, defaults to None
    :type cwd: str, optional
    :param env: environment to launcher process with,
                defaults to None (current env)
    :type env: dict, optional
    :param proc_input: input to the process, defaults to ""
    :type proc_input: str, optional
    :param timeout: timeout of the process, defaults to None
    :type timeout: int, optional
    :raises ShellError: if timeout of process was exceeded
    :raises ShellError: if child process raises an error
    :return: returncode, output, and error of the process
    :rtype: tuple of (int, str, str)
    """
    global verbose_shell

    if verbose_shell:
        source = "shell" if shell else "Popen"

    out_file = open(output, "w+")
    err_file = open(error, "w+")

    # spawning the subprocess and connecting to its output
    proc = psutil.Popen(
        cmd_list, stderr=err_file, stdout=out_file, stdin=PIPE, cwd=cwd, shell=shell, env=env
    )
    try:
        proc_input = proc_input.encode("utf-8")
        out, err = proc.communicate(input=proc_input, timeout=timeout)
    except TimeoutExpired as e:
        proc.kill()
        _, errs = proc.communicate()
        raise Exception(
            "Failed to execute command, timeout reached", e, cmd_list
        ) from None
    except OSError as e:
        raise Exception(
            "Exception while attempting to start a shell process", e, cmd_list
        ) from None

    out_file.close()
    err_file.close()

    # decoding the output and err and return as a string tuple
    return proc.returncode, output, error

@app.task
def execute_command(cmd_list, shell=False, cwd=None, env=None, proc_input="", timeout=None):
    return _execute_cmd(cmd_list, shell, cwd, env, proc_input, timeout)

@app.task
def execute_command_and_write(cmd_list, shell=False, cwd=None, env=None, proc_input="", timeout=None, out=None, error=None):
    return _execute_cmd_and_write(cmd_list, shell, cwd, env, proc_input, timeout, out, error)

@app.task
def create_redis_cluster(hosts, ports):
    ip_list = []
    for host in hosts:
        ip = get_ip_from_host(host)
        for port in ports:
            address = ":".join((ip, str(port) + " "))
            ip_list.append(address)

    # call cluster command
    redis_cli = find_smartsim_file("bin/redis-cli")
    cmd = [redis_cli, "--cluster", "create"]
    cmd += ip_list
    cmd += ["--cluster-replicas", "0"]
    returncode, out, err = _execute_cmd(cmd, proc_input="yes", shell=False)

    if returncode != 0:
        raise Exception("Database '--cluster create' command failed")


@app.task
def check_cluster_status(hosts, ports, trials=10):
    """Check that a cluster is up and running
    :param trials: number of attempts to verify cluster status
    :type trials: int, optional
    :raises SmartSimError: If cluster status cannot be verified
    """
    host_list = []
    for host in hosts:
        for port in ports:
            host_dict = dict()
            host_dict["host"] = get_ip_from_host(host)
            host_dict["port"] = port
            host_list.append(host_dict)

    while trials > 0:
        # wait for cluster to spin up
        time.sleep(5)
        try:
            redis_tester = RedisCluster(startup_nodes=host_list)
            redis_tester.set("__test__", "__test__")
            redis_tester.delete("__test__")
            return
        except (ClusterDownError, RedisClusterException, redis.RedisError):
            trials -= 1
    if trials == 0:
        raise Exception("Cluster setup could not be verified")

@app.task
def find_smartsim_file(path_from_ss_root):
    cur_dir = Path(os.path.dirname(os.path.abspath(__file__)))
    smartsim_dir = cur_dir.parent
    script_path = smartsim_dir.joinpath(path_from_ss_root).resolve()
    return str(script_path)


@app.task
def expand_exe_pathh(exe):
    return _expand_exe_path(exe)

def get_ip_from_host(host):
    """Return the IP address for the interconnect.

    :param host: hostname of the compute node e.g. nid00004
    :type host: str
    :returns: ip of host
    :rtype: str
    """
    ip_address = socket.gethostbyname(host)
    return ip_address

@app.task
def is_file(file_path):
    """Check if a file exists

    :param file_path: path to file
    :type file_path: str
    :returns: True if file exists, False otherwise
    :rtype: bool
    """
    return os.path.isfile(file_path)

@app.task
def get_envv(var):
    """Get the value of an environment variable

    :param var: name of the environment variable
    :type var: str
    :returns: value of the environment variable
    :rtype: str
    """
    return os.environ.get(var)

def _expand_exe_path(exe):
    """Takes an executable and returns the full path to that executable

    :param exe: executable or file
    :type exe: str
    """

    # which returns none if not found
    in_path = which(exe)
    if not in_path:
        if os.path.isfile(exe) and os.access(exe, os.X_OK):
            return os.path.abspath(exe)
        if os.path.isfile(exe) and not os.access(exe, os.X_OK):
            raise Exception(f"File, {exe}, is not an executable")
        raise Exception(f"Could not locate executable {exe}")
    return os.path.abspath(in_path)
