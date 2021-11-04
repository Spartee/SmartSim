import logging
from typing import List

from fastapi import APIRouter, Depends, Path
from sqlalchemy.orm import Session

from ..schemas.model import ModelSchema, ModelCreateSchema, ModelUpdateSchema
from .. import crud
from .utils.db import get_db

logger = logging.getLogger('example')

router = APIRouter()


# list all models of all available experiments
@router.get("/", response_model=List[ModelSchema], name="model:list")
async def model_get_all(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100
):
    return crud.model.get_all(db, skip=skip, limit=limit)

# get a list of models by a given name (may return muliple)
@router.get("/{name}", response_model=List[ModelSchema], name="model:get")
async def model_get(
    name: str,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    return crud.model.get(db, name, skip=skip, limit=limit)

@router.post("/", response_model=ModelSchema, name="model:create")
async def model_create(
    model_in: ModelCreateSchema,
    db: Session = Depends(get_db)):

    return crud.model.create(db, model_in)

# TODO finish this
@router.put("/", response_model=ModelSchema, name="model:update")
async def model_update(
    model_in: ModelUpdateSchema,
    db: Session = Depends(get_db)):

    return crud.model.update(db, model_in)

# TODO finish this
@router.delete("/", response_model=ModelSchema, name="model:delete")
async def model_delete(
    name: str,
    db: Session = Depends(get_db)):

    return crud.model.delete(db, name)

