
from datetime import datetime
from typing import Optional, Dict, Any
from ...common.constants import Status
from .enums import JobType
from pydantic import BaseModel


# ==================================
# Job Base Schema (only server side)
# ==================================

# Shared properties
class JobSchemaBase(BaseModel):
    name: str
    status: str

# Properties needed in DB only
class JobDBSchemaBase(JobSchemaBase):
    id: int
    experiment_id: int
    job_type: JobType
    class Config:
        orm_mode = True

# ======================
# Job CRUD Schema
# ======================

# Additional properties to return to client via API
class JobSchema(JobSchemaBase):

    end_data: datetime
    start_date: datetime
    status: Status
    job_data: Optional[Dict[str, Any]]
    class Config:
        orm_mode = True



