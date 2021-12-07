
from threading import main_thread
from typing import Dict, List, Optional
from .common.enums import EntityType
from .backend.crud import job
from .launcher.step.step import Step
from .launcher.launcher import Launcher

class LaunchableSchema:
    name: str
    cwd: str
    etype: EntityType

class EntitySchema(LaunchableSchema):
    settings: Dict[str, str]
    keyin: Optional[List[str]] = None
    keyout: Optional[bool] = None

class GroupSchema(LaunchableSchema):
    entities: List[EntitySchema]

class BatchSchema:
    settings: Dict[str, str]
    entities: List[EntitySchema]

class ConvergedSchema:
    app: EntitySchema
    db: EntitySchema

class ManifestSchema:
    launchables: List[LaunchableSchema]


# create jobs and place into the database using crud operations
def create_job_steps(manifest: ManifestSchema, launcher: Launcher) -> List[Step]:
    pass

def create_group_steps(manifest: ManifestSchema, launcher: Launcher) -> List[Step]:
    pass

def create_batch_steps(manifest: ManifestSchema, launcher: Launcher) -> List[Step]:
    pass

def create_converged_steps(manifest: ManifestSchema, launcher: Launcher) -> List[Step]:
    pass

# launch the steps and update the jobs in the database
# with their task or job_id as well as update status
def launch_steps(steps: List[Step]):

def launch_groups(groups: List[Groups]):

# TODO break this up
def _launch(self, manifest):
    
    orchestrator = manifest.db
    if orchestrator:
        if self.orchestrator_active:
            msg = "Attempted to launch a second Orchestrator instance. "
            msg += "Only 1 Orchestrator can be active at a time"
            raise SmartSimError(msg)
        self._launch_orchestrator(orchestrator)

    for rc in manifest.ray_clusters:
        rc._update_workers()

    # create all steps prior to launch
    steps = []
    all_entity_lists = manifest.ensembles + manifest.ray_clusters
    for elist in all_entity_lists:
        if elist.batch:
            batch_step = self._create_batch_job_step(elist)
            steps.append((batch_step, elist))
        else:
            # if ensemble is to be run as seperate job steps, aka not in a batch
            job_steps = [(self._create_job_step(e), e) for e in elist.entities]
            steps.extend(job_steps)

    # models themselves cannot be batch steps
    job_steps = [(self._create_job_step(e), e) for e in manifest.models]
    steps.extend(job_steps)

    # launch steps
    for job_step in steps:
        self._launch_step(*job_step)

def _launch_orchestrator(self, orchestrator):
    """Launch an Orchestrator instance

    This function will launch the Orchestrator instance and
    if on WLM, find the nodes where it was launched and
    set them in the JobManager

    :param orchestrator: orchestrator to launch
    :type orchestrator: Orchestrator
    """
    orchestrator.remove_stale_files()

    # if the orchestrator was launched as a batch workload
    if orchestrator.batch:
        orc_batch_step = self._create_batch_job_step(orchestrator)
        self._launch_step(orc_batch_step, orchestrator)

    # if orchestrator was run on existing allocation, locally, or in allocation
    else:
        db_steps = [(self._create_job_step(db), db) for db in orchestrator]
        for db_step in db_steps:
            self._launch_step(*db_step)

    # wait for orchestrator to spin up
    self._orchestrator_launch_wait(orchestrator)

    # set the jobs in the job manager to provide SSDB variable to entities
    # if _host isnt set within each
    self._jobs.set_db_hosts(orchestrator)

    # create the database cluster
    if orchestrator.num_shards > 2:
        num_trials = 5
        cluster_created = False
        while not cluster_created:
            try:
                orchestrator.create_cluster()
                cluster_created = True
            except SmartSimError:
                if num_trials > 0:
                    logger.debug(
                        "Cluster creation failed, attempting again in five seconds..."
                    )
                    num_trials -= 1
                    time.sleep(5)
                else:
                    raise
    self._save_orchestrator(orchestrator)
    logger.debug(f"Orchestrator launched on nodes: {orchestrator.hosts}")

def _launch_step(self, job_step, entity):
    """Use the launcher to launch a job stop

    :param job_step: a job step instance
    :type job_step: Step
    :param entity: entity instance
    :type entity: SmartSimEntity
    :raises SmartSimError: if launch fails
    """

    try:
        job_id = self._launcher.run(job_step)
    except LauncherError as e:
        msg = f"An error occurred when launching {entity.name} \n"
        msg += "Check error and output files for details.\n"
        msg += f"{entity}"
        logger.error(msg)
        raise SmartSimError(f"Job step {entity.name} failed to launch") from e

    if self._jobs.query_restart(entity.name):
        logger.debug(f"Restarting {entity.name}")
        self._jobs.restart_job(job_step.name, job_id, entity.name)
    else:
        logger.debug(f"Launching {entity.name}")
        self._jobs.add_job(job_step.name, job_id, entity)

def _create_batch_job_step(self, entity_list):
    """Use launcher to create batch job step

    :param entity_list: EntityList to launch as batch
    :type entity_list: EntityList
    :return: job step instance
    :rtype: Step
    """
    batch_step = self._launcher.create_step(
        entity_list.name, entity_list.path, entity_list.batch_settings
    )
    for entity in entity_list.entities:
        # tells step creation not to look for an allocation
        entity.run_settings.in_batch = True
        step = self._create_job_step(entity)
        batch_step.add_to_batch(step)
    return batch_step

def _create_job_step(self, entity):
    """Create job steps for all entities with the launcher

    :param entities: list of all entities to create steps for
    :type entities: list of SmartSimEntities
    :return: list of tuples of (launcher_step, entity)
    :rtype: list of tuples
    """
    # get SSDB, SSIN, SSOUT and add to entity run settings
    if not isinstance(entity, DBNode):
        self._prep_entity_client_env(entity)

    step = self._launcher.create_step(entity.name, entity.path, entity.run_settings)
    return step

def _prep_entity_client_env(self, entity):
    """Retrieve all connections registered to this entity

    :param entity: The entity to retrieve connections from
    :type entity:  SmartSimEntity
    :returns: Dictionary whose keys are environment variables to be set
    :rtype: dict
    """
    client_env = {}
    addresses = self._jobs.get_db_host_addresses()
    if addresses:
        if len(addresses) <= 128:
            client_env["SSDB"] = ",".join(addresses)
        else:
            # Cap max length of SSDB
            client_env["SSDB"] = ",".join(addresses[:128])
        if entity.incoming_entities:
            client_env["SSKEYIN"] = ",".join(
                [in_entity.name for in_entity in entity.incoming_entities]
            )
        if entity.query_key_prefixing():
            client_env["SSKEYOUT"] = entity.name
    entity.run_settings.update_env(client_env)

def _sanity_check_launch(self, manifest):
    """Check the orchestrator settings

    Sanity check the orchestrator settings in case the
    user tries to do something silly. This function will
    serve as the location of many such sanity checks to come.

    :param manifest: Manifest with deployables to be launched
    :type manifest: Manifest
    :raises SSConfigError: If local launcher is being used to
                            launch a database cluster
    """
    orchestrator = manifest.db
    if isinstance(self._launcher, LocalLauncher) and orchestrator:
        if orchestrator.num_shards > 1:
            raise SSConfigError(
                "Local launcher does not support launching multiple databases"
            )
    # check for empty ensembles
    entity_lists = manifest.ensembles
    for elist in entity_lists:
        if len(elist) < 1:
            raise SSConfigError("User attempted to run an empty ensemble")

def _save_orchestrator(self, orchestrator):
    """Save the orchestrator object via pickle

    This function saves the orchestrator information to a pickle
    file that can be imported by subsequent experiments to reconnect
    to the orchestrator.

    :param orchestrator: Orchestrator configuration to be saved
    :type orchestrator: Orchestrator
    """

    dat_file = "/".join((orchestrator.path, "smartsim_db.dat"))
    db_jobs = self._jobs.db_jobs
    orc_data = {"db": orchestrator, "db_jobs": db_jobs}
    steps = []
    for db_job in db_jobs.values():
        steps.append(self._launcher.step_mapping[db_job.name])
    orc_data["steps"] = steps
    with open(dat_file, "wb") as pickle_file:
        pickle.dump(orc_data, pickle_file)

def _orchestrator_launch_wait(self, orchestrator):
    """Wait for the orchestrator instances to run

    In the case where the orchestrator is launched as a batch
    through a WLM, we wait for the orchestrator to exit the
    queue before proceeding so new launched entities can
    be launched with SSDB address

    :param orchestrator: orchestrator instance
    :type orchestrator: Orchestrator
    :raises SmartSimError: if launch fails or manually stopped by user
    """
    if orchestrator.batch:
        logger.info("Orchestrator launched as a batch")
        logger.info("While queued, SmartSim will wait for Orchestrator to run")
        logger.info("CTRL+C interrupt to abort and cancel launch")

    ready = False
    while not ready:
        try:
            time.sleep(CONFIG.jm_interval)
            # manually trigger job update if JM not running
            if not self._jobs.actively_monitoring:
                self._jobs.check_jobs()

            # _jobs.get_status acquires JM lock for main thread, no need for locking
            statuses = self.get_entity_list_status(orchestrator)
            if all([stat == STATUS_RUNNING for stat in statuses]):
                ready = True
                # TODO remove in favor of by node status check
                time.sleep(CONFIG.jm_interval)
            elif any([stat in TERMINAL_STATUSES for stat in statuses]):
                self.stop_entity_list(orchestrator)
                msg = "Orchestrator failed during startup"
                msg += f" See {orchestrator.path} for details"
                raise SmartSimError(msg)
            else:
                logger.debug("Waiting for orchestrator instances to spin up...")
        except KeyboardInterrupt as e:
            logger.info("Orchestrator launch cancelled - requesting to stop")
            self.stop_entity_list(orchestrator)
            raise SmartSimError("Orchestrator launch manually stopped") from e
            # TODO stop all running jobs here?

