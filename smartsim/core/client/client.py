

from .control import Manifest
from typing import Dict, List
from ...error import SmartSimError, SSConfigError, SSUnsupportedError
from .common.constants import Status
from .control.jobmonitor import JobMonitor
from .backend.schemas.enums import LauncherType
from .backend.db.session import db_session
from .backend import crud

from ..launcher import (
    SlurmLauncher,
    LocalLauncher,
    LSFLauncher,
    CobaltLauncher,
    PBSLauncher
)

class BackendClient:

    def __init__(self, launcher="local"):
        self.__exp_id = None
        self.init_launcher(launcher)

    @property
    def exp_id(self):
        if not self.__exp_id:
            raise SmartSimError("Backend Client not initialized")
        return self.__exp_id

    def create_exp(self, name: str, description: str, path: str, launcher: LauncherType):
        pass

    def start(self, manifest: Manifest, block: bool=True):
        pass

    def stop(self, maniest: Manifest):
        pass

    def get_status(self, manifest: Manifest) -> List[Status]:
        # used to implement poll and finished
        pass

    def summary(self) -> Dict[str, str]:
        pass

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



class LocalClient(BackendClient):

    def __init__(self):
        monitor = JobMonitor()

    def create_exp(self, name: str, description: str, path: str, launcher: LauncherType) -> int:
        exp = {
            "name": name,
            "description": description,
            "path": path,
            "launcher": launcher
        }
        exp_proto = crud.experiment.create(db_session, exp)
        self.monitor.init_launcher(launcher)
        self.__exp_id = exp_proto.id

    def start(self, manifest: Manifest, block: bool=True):
        

    def stop(self, manifest: Manifest):
        pass

    def get_status(self, manifest: Manifest) -> List[Status]:
        pass

    def summary(self, manifest: Manifest) -> Dict[str, str]:
        pass

class RemoteBackendClient(BackendClient):

    def __init__(self):
        from swagger_client import ApiClient
        pass

    def create_exp(self, name: str, description: str, path: str, launcher: LauncherType) -> int:
        # send https reuqest to backend
        pass

    def start(self, manifest: Manifest, block: bool=True):
        pass

    def stop(self, manifest: Manifest):
        pass