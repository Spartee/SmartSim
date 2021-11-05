import datetime
from sqlalchemy import Column, Integer, String, Boolean, PickleType
from sqlalchemy.orm import column_property, relationship, backref
from sqlalchemy.sql.expression import select
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import Date, DateTime

from ..schemas.enums import JobType, AppType

from ..db.session import DBBase
from ...common.constants import Status, Launcher

class BaseProto(DBBase):
    """Base data model for all objects"""

    __abstract__ = True

    created_on = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)
    updated_on = Column(DateTime, nullable=True, onupdate=datetime.datetime.utcnow)


class ExperimentProto(BaseProto):
    __tablename__ = "experiments"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(60), unique=True, index=True)
    path = Column(String(255))
    launcher = Column(String(20), default=Launcher.local)
    description = Column(String)

    # all below Proto contain a .experiment attribute because of these backrefs
    models = relationship("ModelProto", backref="experiment")
    ensembles = relationship("EnsembleProto", backref="experiment")
    apps = relationship("AppProto", backref="experiment")
    jobs = relationship("JobProto", backref="experiment")


class JobProto(BaseProto):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, unique=True, index=True)
    status = Column(String(20), default=Status.STATUS_NEW, index=True)
    job_type = Column(String(20))
    entity_type = Column(String(20))
    task_ids = Column(PickleType, nullable=True)
    wlm_id = Column(String(20), nullable=True)
    start_date = Column(DateTime, nullable=True)
    end_date = Column(DateTime, nullable=True)
    job_data = Column(PickleType, nullable=True)

    experiment_id = Column(
        Integer, ForeignKey("experiments.id", ondelete="CASCADE"), nullable=False
    )

class ModelProto(BaseProto):
    __tablename__ = "models"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(60), unique=True, index=True)
    path = Column(String(256))
    params = Column(PickleType)
    run_settings = Column(PickleType)

    experiment_id = Column(
        Integer, ForeignKey("experiments.id", ondelete="CASCADE"), nullable=False
    )
    # also contains a .ensemble attribute b/c of backref in ensemble
    ensemble_id = Column(
        Integer, ForeignKey("ensembles.id", ondelete="CASCADE"), nullable=True
    )

class EnsembleProto(BaseProto):
    __tablename__ = "ensembles"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255), unique=True, index=True)
    path = Column(String(255))
    params = Column(PickleType, nullable=True)
    run_settings = Column(PickleType)
    batch_settings = Column(PickleType, nullable=True)

    experiment_id = Column(
        Integer, ForeignKey("experiments.id", ondelete="CASCADE"), nullable=False
    )
    models = relationship("ModelProto", backref="ensemble")


class AppWorkerProto(BaseProto):
    __tablename__ = "app_components"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(60), unique=True, index=True)
    path = Column(String(256))
    params = Column(PickleType)
    run_settings = Column(PickleType)

    is_master = Column(Boolean, default=False)
    # also contains .app field from ApplicationProto.backref
    app_id = Column(Integer, ForeignKey("apps.id", ondelete="CASCADE"), nullable=False)


class AppProto(BaseProto):
    __tablename__ = "apps"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255), unique=True, index=True)
    path = Column(String(255))
    params = Column(PickleType, nullable=True)
    run_settings = Column(PickleType)
    batch_settings = Column(PickleType, nullable=True)

    has_master = Column(Boolean, default=False)
    app_type = Column(String(20))
    batch = Column(Boolean)
    launcher = Column(String(20))
    app_data = Column(PickleType, nullable=True)

    experiment_id = Column(
        Integer, ForeignKey("experiments.id", ondelete="CASCADE"), nullable=False
    )

    components = relationship("AppWorkerProto", backref="app")