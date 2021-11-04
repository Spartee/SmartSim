from typing import Optional, Dict

from pydantic import BaseModel


# =======================
# Experiment Base Schema
# =======================

# Shared properties
class ExpSchemaBase(BaseModel):
    name: str
    description: Optional[str] = None

# Properties needed in DB only
class ExpDBSchemaBase(ExpSchemaBase):
    id: int
    class Config:
        orm_mode = True

# ======================
# Experiment CRUD Schema
# ======================

# Properties to receive via API on creation
class ExpCreateSchema(ExpSchemaBase):
    path: str
    launcher: str

# Properties to receive via API on update
class ExpUpdateSchema(ExpSchemaBase):
    pass

# Additional properties stored in DB
class ExpDBSchema(ExpDBSchemaBase):
    path: str
    launcher: str

# Additional properties to return to client via API
class ExpSchema(ExpSchemaBase):
    class Config:
        orm_mode = True


