
"""
Errors that should never be exposed to the user.

All exceptions within the core directory should be defined here.

"""

class LauncherError(Exception):
    """Raised when there is an error in the launcher"""


class ShellError(LauncherError):
    """Raised when error arises from function within launcher.shell
    Closely related to error from subprocess(Popen) commands"""

    def __init__(self, message, shell_error, command_list):
        msg = self.create_message(message, shell_error, command_list)
        super().__init__(msg)

    def create_message(self, message, shell_error, command_list):
        if isinstance(command_list, list):
            command_list = " ".join(command_list)
        msg = message + "\n"
        msg += f"\nCommand: {command_list}"
        if shell_error:
            msg += f"\nError from shell: {shell_error}"
        return msg
