
from datetime import datetime
from typing import Optional, Dict, Any

from smartsim.core.common.enums import EntityType
from ...common.constants import Status
from .enums import JobType
from pydantic import BaseModel


# ==================================
# Job Base Schema (only server side)
# ==================================

# Shared properties
class JobSchemaBase(BaseModel):
    name: str

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

class JobCreateSchema(JobSchemaBase):
    experiment_id: int
    job_type: JobType
    entity_name: str
    entity_type: EntityType

# Additional properties to return to client via API
class JobSchema(JobSchemaBase):
    end_data: datetime
    start_date: datetime
    status: Status
    entity_name: str
    entity_type: EntityType
    job_data: Optional[Dict[str, Any]]
    
    class Config:
        orm_mode = True



