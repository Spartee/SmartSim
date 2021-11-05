from typing import List, Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from ..schemas.experiment import ExpCreateSchema, ExpSchema, ExpUpdateSchema
from ..models.models import ExperimentProto, ModelProto

def get_exp_by_name(db_session: Session, exp_name: str) -> ExperimentProto:
    return db_session.query(ExperimentProto).filter(ExperimentProto.name == exp_name).first()

def get(db_session: Session, exp_id: int) -> ExperimentProto:
    return db_session.query(ExperimentProto).filter(ExperimentProto.id == exp_id).first()

def get_all(db_session: Session, skip=0, limit=100) -> List[ExperimentProto]:
    d = db_session.query(ExperimentProto).offset(skip).limit(limit).all()
    return d

def create(db_session: Session, exp: ExpCreateSchema) -> ExperimentProto:
    db_obj = ExperimentProto(**exp.dict())
    db_session.add(db_obj)
    db_session.commit()
    db_session.refresh(db_obj)
    return db_obj

def delete(db_session: Session, exp_name: str) -> ExperimentProto:
    exp_obj = get_exp_by_name(db_session, exp_name)
    db_session.delete(exp_obj)
    db_session.commit()
    db_session.refresh(exp_obj)
    return exp_obj

def get_exp_models(db_session: Session, exp_id: int, skip=0, limit=100) -> List[ModelProto]:
    return db_session.query(
        ModelProto).filter(ModelProto.experiment_id == exp_id).offset(skip).limit(limit).all()

def update(
        db_session: Session, exp_update: ExpUpdateSchema) -> ExperimentProto:
    exp_obj = get_exp_by_name(db_session, exp_update.name)

    exp_data = jsonable_encoder(exp_obj)
    update_data = exp_update.dict(exclude_unset=True)
    for field in exp_data:
        if field in update_data:
            setattr(exp_obj, field, update_data[field])
    db_session.add(exp_obj)
    db_session.commit()
    db_session.refresh(exp_obj)
    return exp_obj
