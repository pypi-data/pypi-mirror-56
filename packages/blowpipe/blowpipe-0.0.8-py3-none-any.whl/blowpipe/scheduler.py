"""
the scheduler queries the database and docker to understand the state of the world
it is responsible for
    - keeping the database and docker in sync by starting containers as necessary
    - triggering work as it is required
"""

from blowpipe import App
import json
import time
import uuid
from blowpipe import constants
from blowpipe import docker_utils
from blowpipe.logger import Logger
from datetime import datetime
from blowpipe.model_state import *


class Report(object):
    """
    The Report is the result of a single execute call by the scheduler
    """

    def __init__(self):
        self.workflows_running = []
        self.workflows_in_setup = []
        self.workflows_completed = []
        self.workflows_failed = []
        self.workflows_manually_triggered = []
        self.workflows_schedule_triggered = []
        self.event_triggered = []
        self.steps_completed = []
        self.steps_running = []
        self.steps_started = []

    def total_actions(self) -> int:
        """
        returns the sum of all actions found
        :return:
        """
        total = 0
        total += len(self.workflows_running)
        total += len(self.workflows_in_setup)
        total += len(self.workflows_completed)
        total += len(self.workflows_failed)
        total += len(self.workflows_manually_triggered)
        total += len(self.workflows_schedule_triggered)
        total += len(self.event_triggered)
        total += len(self.steps_completed)
        total += len(self.steps_running)
        total += len(self.steps_started)
        return total

class Scheduler(object):
    def __init__(self, server):
        self.tick = 0
        self.name = "Scheduler"
        self._quit = False
        self.server = server
        self._is_running = False
        self.logger = Logger("Scheduler")
        self.SLEEP_SECONDS = 0.1

    def execute(self):
        """
        Runs the check() then sleeps for SLEEP_SECONDS
        repeats until quit == True
        :return:
        """

        self._is_running = True
        while not self._quit:
            try:
                report = self.check()
            except Exception as e:
                self.logger.error("execute()", e)
            time.sleep(self.SLEEP_SECONDS)
        self._is_running = False
        return report

    def is_running(self):
        return self._is_running

    def quit(self):
        self._quit = True

    def on_quit(self):
        """
        called by the threadpool when it has finished
        :return:
        """
        self.logger.debug("on_quit()")

    def check(self) -> Report:
        """
        runs a single pass of the scheduler, syncing
        against docker, triggering any jobs that require it etc.
        :return:
        """
        self.tick += 1
        logger = self.logger
        logger.indent()
        db = self.server.get_db()
        report = Report()
        session = db.create_session()
        try:
            workflow_instances = db.get_running_workflows(session, is_active_only=True)
            for workflow_instance in workflow_instances:
                print("scheduler.check() workflow_instance '" + workflow_instance.id + "', state=" + str(workflow_instance.get_state()))
                logger.set_workflow_id(workflow_instance.workflow_id)
                logger.set_run_id(workflow_instance.id)
                workflow = workflow_instance.get_workflow()
                workflow_dirty = False

                if workflow_instance.get_state() == WorkflowState.TRIGGER_MANUAL:
                    logger.info("manually triggered, running first steps.")
                    report.workflows_manually_triggered.append(workflow)
                    workflow_instance.set_state(WorkflowState.SETUP)
                    workflow_dirty = True
                    self.start_shared_resources(workflow_instance)

                elif workflow_instance.get_state() == WorkflowState.TRIGGER_AUTOMATIC:
                    logger.info("schedule triggered, running first steps.")
                    report.workflows_schedule_triggered.append(workflow)
                    workflow_instance.set_state(WorkflowState.SETUP)
                    workflow_dirty = True
                    self.start_shared_resources(workflow_instance)

                elif workflow_instance.get_state() == WorkflowState.SETUP:
                    # todo implement for real but this time lets just progress it
                    report.workflows_in_setup.append(workflow)
                    all_exist, container_exists, volume_exists, network_exists = self.do_shared_resources_exist(workflow_instance)
                    if all_exist:
                        workflow_instance.set_state(WorkflowState.RUNNING)
                        self.find_and_start_first_steps(workflow_instance, report, session)
                        workflow_dirty = True

                elif workflow_instance.get_state() == WorkflowState.RUNNING:
                    running_steps = workflow.get_running_steps()
                    steps_updated = False
                    steps_started = False
                    for step in running_steps:
                        c_info = docker_utils.get_container_info(step=step)

                        if constants.DEBUG and constants.DEBUG_DOCKER_RESPONSE:
                            filename = "docker-response-" + str(uuid.uuid4()) + ".json"
                            logger.info(
                                "(constants.DEBUG_DOCKER_RESPONSE=True) WRITING DOCKER RESPONSE as FILE "
                                + filename
                            )
                            f = open(filename, "w")
                            f.write(json.dumps(c_info.data, indent=4))
                            f.close()

                        step.set_container_info(c_info)

                        if c_info.is_container_exited():
                            logger.info(
                                "step '"
                                + step.get_name()
                                + "' docker container is exited"
                            )
                            # then it has just finished from docker; mark it as finished here
                            step.set_state(StepState.SUCCESS)
                            step.set_container_info(c_info)
                            report.steps_completed.append(step)
                            steps_updated = True
                            workflow_dirty = True
                        else:
                            logger.info(
                                "step '"
                                + step.get_name()
                                + "' docker container is not exited"
                            )
                            report.steps_running.append(step)

                    ready_to_run_steps = workflow.get_ready_to_run_steps()
                    for step in ready_to_run_steps:
                        logger.info("step '" + step.get_name() + "' is ready to run.")
                        self.start_step(workflow_instance, step)
                        workflow_dirty = True
                        steps_started = True

                    # now work out if all steps are complete

                    all_steps = workflow.get_all_steps()
                    workflow_complete = True
                    for step in all_steps:
                        if not step.is_complete():
                            workflow_complete = False
                            workflow_dirty = True
                            break

                    if workflow_complete:
                        logger.info(
                            "- all steps completed, marking workflow as complete."
                        )

                        # then this is complete
                        workflow.set_state(WorkflowState.SUCCESS)
                        workflow_instance.finished = datetime.today()
                        workflow_instance.is_active = False
                        workflow_instance.set_state(WorkflowState.SUCCESS)
                        workflow_dirty = True
                        report.workflows_completed.append(workflow_instance)

                        self.stop_shared_resources(workflow_instance)
                    else:
                        report.workflows_running.append(workflow_instance)
                else:
                    raise BlowpipeError(
                        "Unexpected state for Workflow : "
                        + str(workflow_instance.get_state())
                    )

                if workflow_dirty:
                    workflow_instance.save(session)

            logger.set_workflow_id("")
            logger.set_run_id("")

        except Exception as e:
            print(e)
            logger.error("exception: ", e)

        finally:
            logger.set_workflow_id("")
            logger.set_run_id("")
            session.commit()
            session.close()

        self.logger.unindent()
        return report

    def start_shared_resources(self, workflow_instance) -> None:
        client = docker_utils.docker_client()
        try:
            network = client.networks.create(name=workflow_instance.get_shared_state_network_name())
            volume = client.volumes.create(name=workflow_instance.get_shared_state_volume_name())

            mount_point = constants.SHARED_STATE_DEFAULT_MOUNT_POINT

            volumes = { volume.name: { "bind": mount_point, "mode": "rw" } }

            container = docker_utils.start_container(client=client,
                                                     image_name="redis:alpine",
                                                     container_name=workflow_instance.get_shared_state_container_name(),
                                                     command="",
                                                     network=network.name,
                                                     volumes=volumes,
                                                     detach=True,
                                                     auto_remove=True,
                                                     environment={}
            )

            workflow_instance.set_shared_state_network_id(network.id)
            workflow_instance.set_shared_state_volume_id(volume.id)
            workflow_instance.set_shared_state_container_id(container.id)
            workflow_instance.add_container_id(container.id)

        finally:
            client.close()


    def stop_shared_resources(self, workflow_instance) -> None:
        client = docker_utils.docker_client()
        api_client = docker_utils.api_docker_client()
        try:
            all_container_ids = workflow_instance.get_container_ids()
            for container_id in all_container_ids:
                container_info = docker_utils.get_container_info(name=container_id)
                if container_info is not None:
                    container = client.containers.get(container_id)
                    container.stop()
                    print("stop_shared_resources: container '" + container_id + "'.stop() called")
                    while container_info is not None and not container_info.is_container_exited():
                        time.sleep(0.1)
                        print(container_info)
                        print("container status not exited, status is " + container_info.get_container_status() )
                        container_info = docker_utils.get_container_info(name=container_id)
                    print("stop_shared_resources: container '" + container_id + "'.exited.")
                else:
                    print("stop_shared_resources: container '" + container_id + "' was not found.")

            for container_id in all_container_ids:
                print("remove container: " + container_id)
                try:
                    api_client.remove_container(container_id)
                    print("removed container: " + container_id)
                except Exception as e:
                    print("problem removing container: " + container_id)
                    print(e)


            if workflow_instance.get_shared_state_network_id() is not None:
                network = client.networks.get(workflow_instance.get_shared_state_network_id())
                network.remove()

            if workflow_instance.get_shared_state_volume_id() is not None:
                volume = client.volumes.get(workflow_instance.get_shared_state_volume_id())
                volume.remove()

        finally:
            api_client.close()
            client.close()


    def do_shared_resources_exist(self, workflow_instance) -> bool:
        container_exists = docker_utils.count_containers(prefix=workflow_instance.get_shared_state_container_name()) == 1
        volume_exists = docker_utils.count_volumes(prefix=workflow_instance.get_shared_state_volume_name()) == 1
        network_exists = docker_utils.count_networks(prefix=workflow_instance.get_shared_state_network_name()) == 1
        all_exist = container_exists and volume_exists and network_exists
        return all_exist, container_exists, volume_exists, network_exists

    def find_and_start_first_steps(self, workflow_instance, report, session) -> None:
        """
        starts the prerequisites OR the first step for a workflow instance
        :param workflow_instance:
        :param report: 
        :param session: 
        :return: 
        """
        workflow = workflow_instance.get_workflow()
        # prerequisites = workflow.get_prerequisites()
        # if len(prerequisites) > 0:
        #     for pre in prerequisites:
        #         self.logger.info(".find_and_start_first_steps() prereq is '" + pre.get_name() + "'")
        #         self.start_step(pre)
        # else:
        for step in workflow.get_all_steps():
            if step.is_root():
                self.logger.info(
                    ".find_and_start_first_steps() step is '" + step.get_name() + "'"
                )
                self.start_step(workflow_instance, step)
                report.steps_started.append(step)

    def start_step(self, workflow_instance, step):
        if step.is_enabled():
            self.logger.info(
                ".start_step(" + step.get_name() + ") enabled true, running."
            )
            container_name = step.get_image_name() + "-" + str(uuid.uuid4())
            container_name = container_name.replace(":", "_")
            container_name = container_name.replace("/", "-")
            container_name = container_name.replace("\\", "-")
            env_vars = step.environment()
            step.set_container_name(container_name)
            response = docker_utils.start_step(workflow_instance, step, env_vars)
            step.set_started(datetime.today())
            step.set_state(StepState.IN_PROGRESS)
            self.logger.info(
                ".start_step("
                + step.get_name()
                + ") started, state set to "
                + str(StepState.IN_PROGRESS)
            )
            workflow_instance.add_container_id(response.id)
        else:
            self.logger.info(
                ".start_step(" + step.get_name() + ") enabled false, not running."
            )
