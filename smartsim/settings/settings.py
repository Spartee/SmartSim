from pprint import pformat

from ..error import SSConfigError
from ..utils import get_logger
from ..utils.helpers import expand_exe_path, init_default

logger = get_logger(__name__)


class RunSettings:
    def __init__(
        self, exe, exe_args=None, run_command="", run_args=None, env_vars=None
    ):
        """RunSettings represent how an entity or job should be run

        :param exe: executable
        :type exe: str
        :param exe_args: executable arguments, defaults to None
        :type exe_args: str | list[str], optional
        :param run_command: launch binary e.g. srun, defaults to ""
        :type run_command: str, optional
        :param run_args: arguments for run command, defaults to None
        :type run_args: dict[str, str], optional
        :param env_vars: environment vars to launch job with, defaults to None
        :type env_vars: dict[str, str], optional
        """
        self.exe = [expand_exe_path(exe)]
        self.exe_args = self._set_exe_args(exe_args)
        self.run_args = init_default({}, run_args, (dict, list))
        self.env_vars = init_default({}, env_vars, (dict, list))
        self._run_command = run_command
        self.in_batch = False

    @property
    def run_command(self):
        """Return the batch command

        Tests to see if we can expand the batch command
        path, and if not, returns the batch command
        as is
        :returns: batch command
        :type: str
        """
        try:
            if self._run_command:
                cmd = expand_exe_path(self._run_command)
                return cmd
            return None
        except SSConfigError:
            return self._run_command

    def update_env(self, env_vars):
        """update the environment variables a job is launched with"""
        self.env_vars.update(env_vars)

    def add_exe_args(self, args):
        """Add executable arguments to final command produced by run settings

        :param args: executable arguments
        :type args: list[str]
        :raises TypeError: if exe args are not strings
        """
        if isinstance(args, str):
            args = args.split()
        for arg in args:
            if not isinstance(arg, str):
                raise TypeError("Executable arguments should be a list of str")
            self.exe_args.append(arg)

    def _set_exe_args(self, exe_args):
        if exe_args:
            if isinstance(exe_args, str):
                return exe_args.split()
            if isinstance(exe_args, list):
                correct_type = all([isinstance(arg, (str)) for arg in exe_args])
                if not correct_type:
                    raise TypeError("Executable arguments were not list of str or str")
                return exe_args
            raise TypeError("Executable arguments were not list of str or str")
        else:
            return []

    def __str__(self):
        string = f"Executable: {self.exe[0]}\n"
        string += f"Executable arguments: {self.exe_args}\n"
        if self.run_command:
            string += f"Run Command: {self._run_command}\n"
        if self.run_args:
            string += f"Run arguments: {pformat(self.run_args)}"
        return string


class BatchSettings:
    def __init__(self, batch_cmd, batch_args=None):
        self._batch_cmd = batch_cmd
        self.batch_args = init_default({}, batch_args, dict)

    @property
    def batch_cmd(self):
        """Return the batch command

        Tests to see if we can expand the batch command
        path, and if not, returns the batch command
        as is
        :returns: batch command
        :type: str
        """
        try:
            cmd = expand_exe_path(self._batch_cmd)
            return cmd
        except SSConfigError:
            return self._batch_cmd

    def set_nodes(self, num_nodes):
        raise NotImplementedError

    def set_walltime(self, walltime):
        raise NotImplementedError

    def set_account(self, acct):
        raise NotImplementedError

    def format_batch_args(self):
        raise NotImplementedError

    def set_batch_command(self, command):
        self._batch_cmd = command

    def __str__(self):
        string = f"Batch Command: {self._batch_cmd}\n"
        if self.batch_args:
            string += f"Batch arguments: {pformat(self.batch_args)}"
        return string