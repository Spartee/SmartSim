

from typing import Optional, Dict, Any, List

from pydantic import BaseModel


# =======================
# Manifest Base Schema
# =======================

# Shared properties
class ManifestSchemaBase(BaseModel):
    launchables: List[str]

# ======================
# Manifest CRUD Schema
# ======================

# schema for when users send a manifest to be checked
class ManifestCheckSchema(ManifestSchemaBase):
    launcher: str

# Additional properties to return to client via API
class ManifestSchema(ManifestSchemaBase):
    launcher: str

