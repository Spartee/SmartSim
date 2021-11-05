
from typing import List, Optional
from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from sqlalchemy.sql import and_
from ..models.models import EnsembleProto


def get_ensemble_by_name(db_session: Session, ensemble_name: str) -> EnsembleProto:
    models = db_session.query(EnsembleProto).filter(EnsembleProto.name == ensemble_name).all()
    return models
