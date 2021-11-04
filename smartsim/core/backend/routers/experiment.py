import logging
from typing import List
from .. import crud
from ..schemas.experiment import ExpCreateSchema, ExpSchema, ExpUpdateSchema
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .utils.db import get_db

router = APIRouter()

logger = logging.getLogger('example')


@router.get("/",
            response_model=List[ExpSchema],
            name="experiment:list",
            operation_id="list_all_experiments")
async def experiment_get_all(
    db: Session = Depends(get_db),
    limit: int = 100,
):
    return crud.experiment.get_all(db, limit=limit)


@router.get("/{exp_name}",
            response_model=ExpSchema,
            name="experiment:get",
            operation_id="get_experiment")
async def experiment_get(
    exp_name: str,
    db: Session = Depends(get_db)
):
    return crud.experiment.get_exp_by_name(db, exp_name)


@router.post("/",
             response_model=ExpSchema,
             name="experiment:create",
             operation_id="create_experiment")
async def experiment_create(
    exp_in: ExpCreateSchema,
    db: Session = Depends(get_db)):

    return crud.experiment.create(
        db_session=db,
        exp=exp_in,
    )

@router.put("/",
            response_model=ExpUpdateSchema,
            name="experiment:update",
            operation_id="update_experiment")
async def experiment_update(
    exp_update: ExpUpdateSchema,
    db: Session = Depends(get_db)
):
    raise NotImplementedError


@router.delete("/{exp_name}",
               name="experiment:delete",
               operation_id="delete_experiment")
async def experiment_delete(
    exp_name: str,
    db: Session = Depends(get_db),
):
    raise NotImplementedError
