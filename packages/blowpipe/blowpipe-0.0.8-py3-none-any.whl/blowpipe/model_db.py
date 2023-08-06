"""
the blowpipe.model_db package contains the persistence logic for the blowpipe.model package classes
currently it defaults to sqlite ising SQLAlchemy
"""
import os
import time
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import orm, func, Sequence
from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    JSON,
    Enum,
    ForeignKey,
)
import enum
import yaml
import hashlib
import uuid
from blowpipe import constants
from datetime import datetime
from blowpipe.logger import Logger
from blowpipe.exceptions import BlowpipeError
from blowpipe.model_db import *
from blowpipe import model
from blowpipe.model_state import *
import uuid

Base = declarative_base()

SQLITE_DEFAULT = "sqlite:///blowpipe.db"


class Config(Base):
    """
    Config is a cheap key/value way of persisting settings for the server
    """
    __tablename__ = "config"
    key = Column(String, primary_key=True)
    value = Column(String, nullable=False)


class WorkflowDefinition(Base):
    """
    A WorkflowDefinition is the unit of data representing a Workflow/Pipeline
    """

    __tablename__ = "workflow_definitions"
    # id = Column(Integer, Sequence("seq_workflow_id"), primary_key=True, autoincrement=True)
    id = Column(String, primary_key=True)
    created = Column(DateTime, nullable=False, default=datetime.utcnow)
    last_modified = Column(DateTime, nullable=False, default=datetime.utcnow)
    version = Column(Integer, nullable=False)
    yaml = Column(String, nullable=False)
    is_deleted = Column(Boolean, nullable=False, default=False)
    is_enabled = Column(Boolean, nullable=False, default=False)
    deleted_date = Column(DateTime, nullable=True)
    instances = relationship("WorkflowInstance", back_populates="workflow_definition")
    wf = None

    def get_workflow(self) -> model.Workflow:
        if self.wf is None:
            self.wf = model.Workflow(self.yaml)
        return self.wf

    def save(self, session):
        if self.get_workflow() is not None:
            self.yaml = self.get_workflow().to_yaml()
        session.add(self)
        session.commit()

    """
    @orm.reconstructor
    def init_on_load_from_db(self):
        if self.yaml is not None:
            self.workflow = model.Workflow(self.yaml)
        else:
            self.workflow = None
    """

    def __eq__(self, other):
        if other is None:
            return False
        return self.id == other.id

    """
    def save(self, session):
        session.add(self)
        session.commit()

    def delete(self, session):
        session.delete(self)
        session.commit()
    """


class WorkflowHistory(Base):
    """
    A Workflow is the unit of data representing a Workflow/Pipeline
    """

    __tablename__ = "workflow_history"

    id = Column(String, nullable=False, primary_key=True)
    version = Column(Integer, nullable=False, primary_key=True)
    created = Column(DateTime, nullable=False, default=datetime.utcnow)
    reason = Column(String, nullable=False)
    yaml = Column(String, nullable=False)

    """
    def save(self, session):
        session.add(self)
        session.commit()

    def delete(self, session):
        session.delete(self)
        session.commit()
    """


class WorkflowInstance(Base):
    """
    A WorkflowInstance is an running instance of a Workflow
    """

    __tablename__ = "workflow_instances"
    id = Column(String, nullable=False, primary_key=True)
    # id = Column(Integer, Sequence("seq_job_id"), primary_key=True, autoincrement=True)
    created = Column(DateTime, default=datetime.utcnow, nullable=False)
    last_modified = Column(DateTime, default=datetime.utcnow, nullable=False)
    finished = Column(DateTime)
    is_active = Column(Boolean, default=False, nullable=False)
    outcome = Column(String, default=constants.OUTCOME_UNKNOWN, nullable=False)
    state = Column(String, default=model.WorkflowState.INITIAL.value, nullable=False)
    yaml = Column(String, nullable=False)
    workflow_id = Column(String, ForeignKey("workflow_definitions.id"))
    workflow_definition = relationship("WorkflowDefinition", back_populates="instances")

    shared_state_network_id = Column(String, nullable=True)
    shared_state_volume_id = Column(String, nullable=True)
    shared_state_container_id = Column(String, nullable=True)

    wf = None

    """
    @orm.reconstructor
    def init_on_load_from_db(self):
        if self.yaml is not None:
            self.logger.debug(">>>>>>>> Setting the workflow object on the WorkflowInstance >>>>>>>>>>>")
            self.workflow = model.Workflow(self.yaml)
        else:
            self.logger.debug(">>>>>>>> WTF the yaml for the instance was empty >>>>>>>")
            self.workflow = None
    """

    def get_container_ids(self):
        return self.get_workflow().get_container_ids()

    def add_container_id(self, container_id):
        wf = self.get_workflow()
        wf.add_container_id(container_id)

    def set_shared_state_volume_id(self, id):
        self.shared_state_volume_id = id

    def set_shared_state_network_id(self, id):
        self.shared_state_network_id = id

    def set_shared_state_container_id(self, id):
        self.shared_state_container_id = id

    def get_shared_state_volume_id(self):
        return self.shared_state_volume_id

    def get_shared_state_network_id(self):
        return self.shared_state_network_id

    def get_shared_state_container_id(self):
        return self.shared_state_container_id

    def get_shared_state_network_name(self):
        return self.id

    def get_shared_state_volume_name(self):
        return self.id

    def get_shared_state_container_name(self):
        return self.id

    def get_workflow(self) -> model.Workflow:
        if self.wf is None:
            self.wf = model.Workflow(self.yaml)
        return self.wf

    def get_step(self, step_name) -> model.Step:
        return self.get_workflow().get_step(step_name)

    def save(self, session):
        if self.get_workflow() is not None:
            self.yaml = self.get_workflow().to_yaml()
        session.add(self)
        session.commit()

    def delete(self, session):
        session.delete(self)
        session.commit()

    def get_state(self) -> model.WorkflowState:
        return model.WorkflowState(self.state)

    def set_state(self, state: model.WorkflowState):
        current = self.get_state()
        if current.is_transition_legit(state):
            current_state = current.value
            new_state = state.value
            print("WorkflowInstance.set_state(" + current_state + " > " + new_state + ")")
            self.state = state.value
        else:
            raise BlowpipeError("Invalid state transition {} to {} ".format(current, state))


class DB:
    """
    the DB is the helper class providing the route to the datastore
    """

    def __init__(self, config, sqlite_filename=SQLITE_DEFAULT):
        self.config = config
        self.sqlite_filename = sqlite_filename
        self._is_connected = False

    def build_instance(self, workflow, session) -> WorkflowInstance:
        job = WorkflowInstance()
        job.id = str(uuid.uuid4())
        job.yaml = self.token_switch(workflow.yaml, session)
        workflow.instances.append(job)
        session.add(workflow)
        session.commit()
        return job

    def get_sqlite_filename(self) -> str:
        return self.sqlite_filename

    def token_switch(self, yml, session) -> str:
        """
        token switches a passed string against all variables that exists
        :param yml:
        :return:
        """
        config = self.get_all_config(session)
        for c in config:
            token = "${" + c.key + "}"
            value = c.value
            yml = yml.replace(token, value)
        return yml

    def is_connected(self) -> bool:
        """
        indicates if we are connected to the relational database
        :return:
        """
        return self._is_connected

    def connect(self):
        self.engine = create_engine(self.sqlite_filename, connect_args={"check_same_thread": False})
        self.Session = sessionmaker(bind=self.engine)
        self._is_connected = True

    def disconnect(self):
        # s = self.session()
        # s.close()
        # self.engine.disconnect()
        self._is_connected = False

    def reset(self):
        max_attempts = 2
        attempt_count = 0
        curr_dir = os.getcwd()
        while attempt_count < max_attempts:
            try:
                attempt_count += 1
                db_filename = self.get_sqlite_filename()

                if not os.path.isdir(self.config.get_root_dir()):
                    os.makedirs(self.config.get_root_dir())
                    os.chdir(self.config.get_root_dir())
                elif os.path.isfile(db_filename) and os.path.exists(db_filename):
                    os.chdir(self.config.get_root_dir())
                    os.remove(db_filename)
                time.sleep(0.1)
                self.connect()
                self.drop_schema()
                self.create_schema()
                break
            except Exception as e:
                if attempt_count > max_attempts:
                    raise e
            finally:
                os.chdir(curr_dir)
        os.chdir(curr_dir)

    def create_schema(self):
        Base.metadata.create_all(self.engine)

    def drop_schema(self):
        Base.metadata.drop_all(self.engine)

    def create_session(self):
        return self.Session()

    def enable_workflow(self, workflow_id, session) -> bool:
        defn = self.get_workflow_definition(workflow_id, session)
        if defn is None:
            return False
        else:
            defn.is_enabled = True
            session.add(defn)
            self.update_workflow_definition(workflow_id, defn.yaml, "Enabled", session)
            session.commit()
            return True

    def disable_workflow(self, workflow_id, session) -> bool:
        defn = self.get_workflow_definition(workflow_id, session)
        if defn is None:
            return False
        else:
            defn.is_enabled = False
            session.add(defn)
            self.update_workflow_definition(workflow_id, defn.yaml, "Disabled", session)
            session.commit()
            return True

    def add_workflow_definition(self, workflow, session) -> WorkflowDefinition:
        yaml = str(workflow.to_yaml())
        defn = WorkflowDefinition()
        version = 1
        defn.id = str(uuid.uuid4())
        defn.version = version
        defn.yaml = yaml

        session.add(defn)

        defn_history = WorkflowHistory(id=defn.id, created=defn.created, version=version, yaml=defn.yaml, reason="Created")
        session.add(defn_history)
        # defn_history.save(session)

        session.commit()
        return defn

    def update_workflow_definition(self, workflow_id, yaml, reason, session):
        defn = self.get_workflow_definition(workflow_id, session)
        version = defn.version
        next_version = version + 1
        defn.yaml = yaml
        defn.version = next_version
        session.add(defn)
        # defn.save(session)

        defn_history = WorkflowHistory(id=defn.id, version=next_version, yaml=defn.yaml, reason=reason)
        session.add(defn_history)
        # defn_history.save(session)

        session.commit()
        return defn

    def get_workflow_definition(self, workflow_id, session) -> WorkflowDefinition:
        return session.query(WorkflowDefinition).filter(WorkflowDefinition.id == workflow_id).first()

    def get_config(self, key, session) -> Config:
        return session.query(Config).filter(Config.key == key).first()

    def get_all_config(self, session):
        q = session.query(Config)
        results = []
        for c in q:
            results.append(c)
        return results

    def set_config(self, key, value, session):
        c = self.get_config(key, session)
        if c is None:
            c = Config(key=key, value=value)
        else:
            c.value = value
        session.add(c)

    def delete_config(self, key, session):
        c = self.get_config(key, session)
        if c is not None:
            session.delete(c)
            return True
        else:
            return False

    def delete_workflow_definition(self, workflow_id, session):
        defn = self.get_workflow_definition(workflow_id, session)
        if defn is not None:
            self.update_workflow_definition(workflow_id, defn.yaml, "Deleted", session)
            defn.is_deleted = True
            defn.deleted_date = datetime.today()
            session.add(defn)
            return True
        else:
            return False

    def count_workflow_definitions(self, session):
        return session.query(WorkflowDefinition).count()

    def get_workflow_definitions(self, include_deleted=False, session=None):
        if include_deleted:
            return session.query(WorkflowDefinition)
        else:
            return session.query(WorkflowDefinition).filter(WorkflowDefinition.is_deleted == include_deleted)

    def get_workflow_definitions_history(self, workflow_id, session):
        return session.query(WorkflowHistory).filter(WorkflowHistory.id == workflow_id)

    def get_workflow_definition_history_with_version(self, workflow_id, version, session):
        return session.query(WorkflowHistory).filter(WorkflowHistory.id == workflow_id).filter(WorkflowHistory.version == version).first()

    def get_running_workflow(self, instance_id, session):
        return session.query(WorkflowInstance).filter(WorkflowInstance.id == instance_id).first()

    def get_running_workflows(self, session, is_active_only):
        if is_active_only:
            return session.query(WorkflowInstance).filter(WorkflowInstance.is_active == True)  # == True
        else:
            return session.query(WorkflowInstance)

    def count_running_workflows(self, session):
        return self.get_running_workflows(session=session, is_active_only=True).count()

    def get_workflow_instances_with_state(self, state: WorkflowState, session, is_active_only: bool):
        result = session.query(WorkflowInstance).filter(WorkflowInstance.state == state.value)
        if is_active_only:
            result = result.filter(WorkflowInstance.is_active)
        return result

