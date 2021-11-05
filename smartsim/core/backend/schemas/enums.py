
from enum import Enum

class JobType(str, Enum):
    jobstep = "jobstep"
    jobgroup = "jobgroup"
    jobbatch = "jobbatch"

class AppType(str, Enum):
    redis = "redis"
    ray = "ray"

class LauncherType(str, Enum):
    slurm = "slurm"
    pbs = "pbs"
    lsf = "lsf"
    cobalt = "cobalt"
    local = "local"

class EntityType(str, Enum):
    model = "model"
    ensemble = "ensemble"
    app = "app"
    appworker = "appworker"