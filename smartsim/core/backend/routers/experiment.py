import logging
from typing import List
from .. import crud
from ..schemas.experiment import ExpCreateSchema, ExpSchema, ExpUpdateSchema
from ..schemas.model import ModelSchema, ModelCreateSchema
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
    skip: int = 0,
    limit: int = 100
):
    return crud.experiment.get_all(db, skip=skip, limit=limit)


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
            response_model=ExpSchema,
            name="experiment:update",
            operation_id="update_experiment")
async def experiment_update(
    exp_update: ExpUpdateSchema,
    db: Session = Depends(get_db)
):
    return crud.experiment.update(db, exp_update)

@router.delete("/{exp_name}",
               response_model=ExpSchema,
               name="experiment:delete",
               operation_id="delete_experiment")
async def experiment_delete(
    exp_name: str,
    db: Session = Depends(get_db),
):
    return crud.experiment.delete(db, exp_name)


#### Models ####


@router.get("/{exp_name}/models/",
            response_model=List[ModelSchema],
            name="experiment:get_all_models",
            operation_id="get_all_models")
async def experiment_get(
    exp_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    return crud.experiment.get_exp_models(db, exp_id, skip, limit)

@router.get("/{exp_name}/models/{model_name}",
            response_model=ModelSchema,
            name="experiment:get_model",
            operation_id="get_model")
async def experiment_get(
    exp_name: str,
    model_name: str,
    db: Session = Depends(get_db)
):
    exp_obj = crud.experiment.get_exp_by_name(db, exp_name)
    for model in exp_obj.models:
        if model.name == model_name:
            return model
    # TODO return error here if the model doesn't exist


@router.post("/{exp_name}/models/",
             response_model=ModelSchema,
             name="experiment:create_model")
async def model_create(
    exp_name: str,
    model_in: ModelCreateSchema,
    db: Session = Depends(get_db)):

    return crud.model.create(db, exp_name, model_in)

