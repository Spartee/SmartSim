from typing import List, Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from ...common.constants import LIVE_STATUSES
from ..schemas.job import JobSchema, JobCreateSchema
from ..models.models import JobProto

# big point
# there will be crud ops for both the JM itself and
# the functions used to fufill requests from the
# API (remotebackend) or the expierment locally (localbackkend)



#### used by the jobmonitor for all jobs #####
def get_active_jobs(db_session: Session) -> List[JobSchema]:
    # how are we filtering these by experiment and user?
    jobs = db_session.query(JobProto).filter(JobProto.status in LIVE_STATUSES).all()

def get_jobs_by_type():
    pass

### used by the api to fufill requests ###
# should alll have an experiment id associated with the request
def get_active_jobs_by_exp(db_session: Session, exp_id: int, job_name: str):
    pass

def create(db_session: Session, job: JobCreateSchema):
    db_obj = JobProto(**job.dict())
    db_session.add(db_obj)
    db_session.commit()
    db_session.refresh(db_obj)
    return db_obj

def bulk_create(db_session: Session, jobs: List[JobCreateSchema]):
    for job in jobs:
        db_obj = JobProto(**job.dict())
        db_session.add(db_obj)
    db_session.commit()
    #db_session.refresh()
