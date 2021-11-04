

from typing import Optional, Dict

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
    status: str
    experiment_id: int

    class Config:
        orm_mode = True

# ======================
# Job CRUD Schema
# ======================

# Additional properties to return to client via API
class JobSchema(JobSchemaBase):

    class Config:
        orm_mode = True



