from pathlib import Path

class SetupError(Exception):
    pass

class Warning_:

    def __init__(self, message):
        prefix = colorize("WARNING: ", "red", bold=True)
        self.message = prefix + message

    def __str__(self):
        return self.message

def _get_install_path():
    try:
        import smartsim as _
    except (ImportError, ModuleNotFoundError):
        raise SetupError("Could not import SmartSim") from None

    # find the path to the setup script
    package_path = Path(_.__path__[0]).resolve()
    if not package_path.is_dir():
        raise SetupError("Could not find SmartSim installation site")

    return package_path

def colorize(string, color, bold=False, highlight=False):
    """
    Colorize a string.
    This function was originally written by John Schulman.
    And then borrowed from spinningup
    https://github.com/openai/spinningup/blob/master/spinup/utils/logx.py
    """

    color2num = dict(
    gray=30,
    red=31,
    green=32,
    yellow=33,
    blue=34,
    magenta=35,
    cyan=36,
    white=37,
    crimson=38,
    )

    attr = []
    num = color2num[color]
    if highlight:
        num += 10
    attr.append(str(num))
    if bold:
        attr.append("1")
    return "\x1b[%sm%s\x1b[0m" % (";".join(attr), string)