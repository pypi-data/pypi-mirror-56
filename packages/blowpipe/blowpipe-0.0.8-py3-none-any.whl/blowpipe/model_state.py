"""
the blowpipe.model package represents all the in-memory data structures we required
they can be persisted using the blowpipe.model_db package
"""
import enum
from blowpipe.exceptions import BlowpipeError


@enum.unique
class StepState(enum.Enum):
    INITIAL = "initial"
    IDLE = "idle"
    IN_PROGRESS = "in_progress"
    SUCCESS = "success"
    FAILURE = "failure"

    def __str__(self):
        return self.value

    def __repr__(self):
        return self.value

    def is_transition_legit(self, next_state) -> bool:
        if self is StepState.INITIAL:
            return True
        elif self is StepState.IDLE:
            return next_state == StepState.IN_PROGRESS
        elif self is StepState.IN_PROGRESS:
            return next_state in [StepState.SUCCESS, StepState.FAILURE]
        else:
            raise BlowpipeError("Cannot determine StepState")


@enum.unique
class WorkflowState(enum.Enum):
    INITIAL = "initial"
    TRIGGER_MANUAL = "trigger_manual"
    TRIGGER_AUTOMATIC = "trigger_automatic"
    SETUP = "setup"
    RUNNING = "running"
    SUCCESS = "success"
    FAILURE = "failure"
    PAUSED = "paused"
    CANCELLED = "cancelled"

    def __str__(self):
        return self.value

    def __repr__(self):
        return self.value

    def is_transition_legit(self, next_state) -> bool:
        if self is WorkflowState.INITIAL:
            return True
        elif self in [WorkflowState.TRIGGER_MANUAL, WorkflowState.TRIGGER_AUTOMATIC]:
            return next_state in [WorkflowState.SETUP, WorkflowState.CANCELLED]
        elif self is WorkflowState.SETUP:
            return next_state in [WorkflowState.RUNNING, WorkflowState.PAUSED, WorkflowState.CANCELLED]
        elif self is WorkflowState.RUNNING:
            return next_state in [WorkflowState.PAUSED,
                                  WorkflowState.CANCELLED,
                                  WorkflowState.SUCCESS,
                                  WorkflowState.FAILURE]
        elif self in [ WorkflowState.SUCCESS, WorkflowState.FAILURE, WorkflowState.CANCELLED ]:
            return False
        elif self is WorkflowState.PAUSED:
            return next_state in [WorkflowState.RUNNING, WorkflowState.CANCELLED]
        else:
            raise BlowpipeError("Cannot determine WorkflowState")


# @enum.unique
# class WorkflowInstanceState(enum.Enum):
#     ACTIVE = "active"
#     INACTIVE = "inactive"
#     ARCHIVED = "archived"
#
#     def __str__(self):
#         return self.value
#
#     def __repr__(self):
#         return self.value
#
#     def is_transition_legit(self, next_state) -> bool:
#         if self is WorkflowInstanceState.ACTIVE:
#             return [WorkflowInstanceState.INACTIVE, WorkflowInstanceState.ARCHIVED]
#         elif self is WorkflowInstanceState.INACTIVE:
#             return [WorkflowInstanceState.ACTIVE, WorkflowInstanceState.ARCHIVED]
#         elif self is WorkflowInstanceState.ARCHIVED:
#             return [WorkflowInstanceState.ACTIVE, WorkflowInstanceState.INACTIVE]
#         else:
#             raise BlowpipeError("Cannot determine WorkflowInstanceState")
