import datetime
from sqlalchemy import Column, Integer, String, Boolean, PickleType
from sqlalchemy.orm import column_property, relationship, backref
from sqlalchemy.sql.expression import select
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import Date, DateTime


from ..db.session import DBBase
from ...common.enums import Status, Launcher

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

    jobs = relationship("JobProto", backref="experiment")


class JobProto(BaseProto):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, unique=True, index=True)
    status = Column(String(20), default=Status.STATUS_NEW, index=True)
    job_type = Column(String(20))
    entity_type = Column(String(20))
    entity_name = Column(String(60))
    task_ids = Column(PickleType, nullable=True)
    wlm_id = Column(String(20), nullable=True)
    start_date = Column(DateTime, nullable=True)
    end_date = Column(DateTime, nullable=True)
    job_data = Column(PickleType, nullable=False, default={})

    experiment_id = Column(
        Integer, ForeignKey("experiments.id", ondelete="CASCADE"), nullable=False
    )

    def set_hosts(self, hosts):
        """Set the hosts for the job

        :param hosts: A list of hosts
        :type hosts: list
        """
        self.job_data["hosts"] = hosts

    def get_hosts(self):
        """Get compute hosts for a job

        :returns: A list of compute hosts if set
        :rtype: list | None
        """
        #TODO come back to this
        try:
            return self.job_data["hosts"]
        except KeyError:
            return None

    def error_report(self):
        """A descriptive error report based on job fields

        :return: error report for display in terminal
        :rtype: str
        """
        warning = f"{self.ename} failed. See below for details \n"
        if self.error:
            warning += (
                f"{self.entity.type} {self.ename} produced the following error \n"
            )
            warning += f"Error: {self.error} \n"
        if self.output:
            warning += f"Output: {self.output} \n"
        warning += f"Job status at failure: {self.status} \n"
        warning += f"Launcher status at failure: {self.raw_status} \n"
        warning += f"Job returncode: {self.returncode} \n"
        warning += f"Error and output file located at: {self.entity.path}"
        return warning

    def __str__(self):
        """Return user-readable string of the Job

        :returns: A user-readable string of the Job
        :rtype: str
        """
        if self.wlm_id:
            job = "{}({}): {}"
            return job.format(self.entity_name, self.wlm_id, self.status)
        else:
            job = "{}: {}"
            return job.format(self.entity_name, self.status)

