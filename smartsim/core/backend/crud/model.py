from typing import List, Optional
from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from sqlalchemy.sql import and_
from ..schemas.model import ModelCreateSchema
from ..models.models import EnsembleProto, ExperimentProto, ModelProto
from ...common.error import ValidationError


def get(db_session: Session, model_name: str) -> ModelProto:
    models = db_session.query(ModelProto).filter(ModelProto.name == model_name).all()
    return models

def get_all(db_session: Session, skip=0, limit=100) -> List[ModelProto]:
    return db_session.query(ModelProto).offset(skip).limit(limit).all()

def create(db_session: Session, exp_name: str, model_schema: ModelCreateSchema) -> ModelProto:
    exp_obj = db_session.query(ExperimentProto).filter(ExperimentProto.name == exp_name).first()
    model_obj = ModelProto(
        experiment_id=exp_obj.id,
        **model_schema.dict()
    )
    exp_obj.models.append(model_obj)

#    ensemble_obj = None
#    if model_schema.ensemble_name:
#        for ensemble in exp_obj.ensembles:
#            if ensemble.name == model_schema.ensemble_name:
#                ensemble_obj.models.append()

    db_session.add(model_obj)
    db_session.commit()
    db_session.refresh(model_obj)
    db_session.refresh(exp_obj)
    return model_obj

