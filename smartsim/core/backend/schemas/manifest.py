

from typing import Optional, Dict, Any, List

from pydantic import BaseModel



# =======================
# Manifest Base Schema
# =======================

# Shared properties
class ManifestSchemaBase(BaseModel):
    experiment_id: int
    models: List[int]
    ensembles: List[int]
    applications: List[int]

# ======================
# Manifest CRUD Schema
# ======================

# Additional properties to return to client via API
class ManifestSchema(ManifestSchemaBase):
    pass
