
from datetime import datetime
from typing import Optional, Dict, Any

from pydantic import BaseModel

from .experiment import ExpSchema


# =======================
# Model Base Schema
# =======================

# Shared properties
class ModelSchemaBase(BaseModel):
    name: str
    path: str
    params: Dict[str, Any]
    run_settings: Dict[str, Any]

# Properties needed in DB only
class ModelDBSchemaBase(ModelSchemaBase):
    id: int
    experiment_id: int

    class Config:
        orm_mode = True

# ======================
# Experiment CRUD Schema
# ======================

# Properties to receive via API on creation
class ModelCreateSchema(ModelSchemaBase):
    pass

# Properties to receive via API on update
class ModelUpdateSchema(ModelSchemaBase):
    pass

# Additional properties stored in DB
class ModelDBSchema(ModelDBSchemaBase):
    experiment_id: int
    ensemble_id: int

# Additional properties to return to client via API
class ModelSchema(ModelSchemaBase):
    id: int
    created_on: datetime
    updated_on: Optional[datetime]

    class Config:
        orm_mode = True
