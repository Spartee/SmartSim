from typing import List, Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from ..schemas.experiment import ExpCreateSchema, ExpSchema
from ..models.models import ExperimentProto

def get_exp_by_name(db_session: Session, exp_name: str) -> ExperimentProto:
    return db_session.query(ExperimentProto).filter(ExperimentProto.name == exp_name).first()

def get(db_session: Session, exp_id: str) -> ExperimentProto:
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


#def update(
#        db_session: Session, *, db_obj: JobModel, obj_in: JobUpdateSchema
#) -> JobModel:
#    obj_data = jsonable_encoder(db_obj)
#    update_data = obj_in.dict(exclude_unset=True)
#    for field in obj_data:
#        if field in update_data:
#            setattr(db_obj, field, update_data[field])
#    db_session.add(db_obj)
#    db_session.commit()
#    db_session.refresh(db_obj)
#    return db_obj
