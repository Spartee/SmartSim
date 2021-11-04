
import logging
from typing import List
from .. import crud
from ..schemas.manifest import ManifestCheckSchema, ManifestSchema
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .utils.db import get_db

router = APIRouter()

logger = logging.getLogger('example')



@router.post("/check",
            response_model=ManifestSchema,
            name="execute:check",
            operation_id="check_manifest",
            status_code=200)
async def check(
    manifest: ManifestCheckSchema,
    db: Session = Depends(get_db),
):
    return manifest.get_names()


@router.post("/start",
            response_model=ManifestSchema,
            name="execute:start",
            operation_id="start",
            status_code=200)
async def start(
    manifest: ManifestSchema,
    db: Session = Depends(get_db),
):
    """Start the names listed in the manifest and return the names"""
    return manifest.get_names()


@router.get("/stop",
            response_model=ManifestSchema,
            name="execute:stop",
            operation_id="stop")
async def stop(
    manifest: ManifestSchema,
    db: Session = Depends(get_db)
):
    return None


@router.post("/status",
             response_model=JobStatusSchema,
             name="execute:status",
             operation_id="get_status")
async def experiment_create(
    manifest: ManifestSchema,
    db: Session = Depends(get_db)):
    pass

