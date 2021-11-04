import datetime
from sqlalchemy import Column, Integer, String, Boolean, PickleType
from sqlalchemy.orm import column_property, relationship, backref
from sqlalchemy.sql.expression import select
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import Date, DateTime

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


class JobProto(BaseProto):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, unique=True, index=True)
    status = Column(String(20), default=Status.STATUS_NEW, index=True)
    start_date = DateTime()
    end_date = DateTime()
    task_id = Column(Integer)

    entity_id = Column(
        Integer, ForeignKey("entities.id", ondelete="CASCADE"), nullable=False
    )


class JobGroupProto(BaseProto):
    __tablename__ = "jobgroups"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, unique=True, index=True)
    status = Column(String(20), default=Status.STATUS_NEW, index=True)
    start_date = DateTime()
    end_date = DateTime()
    task_ids = Column(PickleType) # list of ints

    entitylist_id = Column(
        Integer, ForeignKey("entitylists.id", ondelete="CASCADE"), nullable=False
    )


class JobBatchProto(BaseProto):
    __tablename__ = "jobbatches"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, unique=True, index=True)
    status = Column(String(20), default=Status.STATUS_NEW, index=True)
    start_date = DateTime()
    end_date = DateTime()
    task_ids = Column(PickleType) # list of ints

    entitylist_id = Column(
        Integer, ForeignKey("entitylists.id", ondelete="CASCADE"), nullable=False
    )


class EntityProto(BaseProto):
    __tablename__ = "entities"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    entity_type = Column(String(50))
    name = Column(String(60), unique=True, index=True)
    path = Column(String(256))
    params = Column(PickleType)
    run_settings = Column(PickleType)

    experiment_id = Column(
        Integer, ForeignKey("experiments.id", ondelete="CASCADE"), nullable=False
    )


    __mapper_args__ = {
        'polymorphic_identity':'entity',
        'polymorphic_on':entity_type
    }

class ModelProto(EntityProto):
    __tablename__ = "models"

    id = Column(Integer, ForeignKey('entities.id'), primary_key=True)

    ensemble_id = Column(
        Integer, ForeignKey("ensembles.id", ondelete="CASCADE"), nullable=True
    )
    ensemble = relationship(
        "EnsembleProto",
        backref=backref("models", passive_deletes=True, lazy="dynamic"),
    )

    __mapper_args__ = {
        'polymorphic_identity':'model'
    }

class EntityListProto(BaseProto):

    __tablename__ = "entitylists"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    entitylist_type = Column(String(20))
    name = Column(String(255), unique=True, index=True)
    path = Column(String(255))
    params = Column(PickleType, nullable=True)
    run_settings = Column(PickleType)
    batch_settings = Column(PickleType, nullable=True)

    experiment_id = Column(
        Integer, ForeignKey("experiments.id", ondelete="CASCADE"), nullable=False
    )

    __mapper_args__ = {
        'polymorphic_identity':'entitylist',
        'polymorphic_on':entitylist_type
    }

class EnsembleProto(EntityListProto):
    __tablename__ = "ensembles"

    id = Column(Integer, ForeignKey('entitylists.id'), primary_key=True)
    models = relationship("ModelProto", back_populates="ensemble")

    __mapper_args__ = {
        'polymorphic_identity':'ensemble',
    }


#class OrchestratorProto(EntityListProto):
#    __tablename__ = "orchestrators"



