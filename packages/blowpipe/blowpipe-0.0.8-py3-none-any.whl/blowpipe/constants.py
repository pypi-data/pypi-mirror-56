CLIENT_VERSION = "0.0.8"
SERVER_VERSION = "0.0.8"

# When the cli contains -v, this will be true.
# What it means is that we should log to the console a
# Bit more on a case-by-case basis.
VERBOSE = False

# See the STATE data model
# STATE_ENABLED = "enabled"
# STATE_DISABLED = "disabled"
#
# STATE_ACTIVE = "active"
# STATE_TRIGGER_MANUAL = "trigger_manual"
# STATE_TRIGGER_SCHEDULE = "trigger_schedule"
# STATE_IDLE = "idle"
# STATE_IN_PROGRESS = "in_progress"
# STATE_SUCCESS = "success"
# STATE_FAILURE = "failure"
# STATE_PAUSED = "paused"
# STATE_RESUME = "resume"
# STATE_COMPLETE = "complete"
# STATE_UNKNOWN = "unknown"

# the location to mount the shared volume
SHARED_STATE_DEFAULT_MOUNT_POINT = "/shared-state"

OUTCOME_UNKNOWN = "unknown"
OUTCOME_IN_PROGRESS = "in_progress"
OUTCOME_FAILURE = "failure"
OUTCOME_CANCELLED = "cancelled_manually"

# If true, will write to current dir, docker-response-uuid.json
DEBUG = True
DEBUG_DOCKER_RESPONSE = False

DEFAULT_GRPC_CLIENT_IP = "127.0.0.1"
DEFAULT_GRPC_SERVER_IP = "127.0.0.1"
DEFAULT_HTTP_PORT = 41414
DEFAULT_GRPC_PORT = 41415
DEFAULT_CONFIG = """
[http]
enabled=False
port=TOKEN_HTTP_PORT
ip=0.0.0.0

[grpc]
enabled=True
server_port=TOKEN_GRPC_PORT
server_ip=TOKEN_GRPC_SERVER_IP
client_ip=TOKEN_GRPC_CLIENT_IP

[database]
type=sqlite
"""
