from typing import List, Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from sqlalchemy.sql import and_
from ..schemas.model import ModelCreateSchema
from ..models.models import ModelProto

# experiment CRUD functions
from .experiment import get_exp_by_name

def get(db_session: Session, model_name: str, skip=0, limit=100) -> ModelProto:
    models = db_session.query(ModelProto).filter(ModelProto.model_name == model_name).all()
    return models

def get_all(db_session: Session, skip=0, limit=100) -> List[ModelProto]:
    return db_session.query(ModelProto).offset(skip).limit(limit).all()

def create(db_session: Session, model_schema: ModelCreateSchema) -> ModelProto:
    exp_obj = get_exp_by_name(db_session, model_schema.experiment_name)
    # TODO raise HTTP Error if Experiment doesn't exist

    model_obj = ModelProto(
        experiment_id=exp_obj.id,
        experiment=exp_obj,
        **model_schema.dict()
    )
    db_session.add(model_obj)
    db_session.commit()
    db_session.refresh(model_obj)
    return model_obj

