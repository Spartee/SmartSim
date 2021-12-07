
from enum import Enum

class JobType(str, Enum):
    jobstep = "jobstep"
    jobgroup = "jobgroup"
    batchjob = "batchjob"
    convergedjob = "convergedjob"

class LauncherType(str, Enum):
    slurm = "slurm"
    pbs = "pbs"
    lsf = "lsf"
    cobalt = "cobalt"
    local = "local"

class EntityType(str, Enum):
    model = "model"
    ensemble = "ensemble"
    db = "orchestrator"
    app = "app"
    appworker = "appworker"
    converged = "converged"

# Statuses that are applied to jobs
class Status(str, Enum):
    STATUS_RUNNING = "Running"
    STATUS_COMPLETED = "Completed"
    STATUS_CANCELLED = "Cancelled"
    STATUS_FAILED = "Failed"
    STATUS_NEW = "New"
    STATUS_PAUSED = "Paused"
