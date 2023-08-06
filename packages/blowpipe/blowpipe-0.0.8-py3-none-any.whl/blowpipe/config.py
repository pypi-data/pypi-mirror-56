import os
import json
from common.ini import IniFile
from blowpipe import constants


class BlowpipeConfig(object):
    def __init__(self, filename=None):
        if filename is not None:
            basename = filename.split("/")[-1]
            self.filename = filename
            self.root_dir = self.filename[0 : len(filename) - len(basename) - 1]
            self.data = self.load(filename)
        else:
            self.data = IniFile()
            self.filename = None

    def load(self, filename):
        filename = self.get_filename()
        return IniFile(filename)

    def save(self):
        """
        persists any settings to the preferences file
        :return:
        """
        root_dir = self.get_root_dir()
        if not os.path.isdir(root_dir):
            os.makedirs(root_dir)
        filename = self.get_filename()
        f = open(filename, "w")
        f.write(json.dumps(self.data, indent=4))
        f.close()

    def is_web_server_enabled(self):
        return self.data.get("http", "enabled", "False") == "True"

    def is_grpc_server_enabled(self):
        return self.data.get("grpc", "enabled", "False") == "True"

    def get_grpc_port(self):
        default_url = constants.DEFAULT_GRPC_SERVER_IP + ":" + str(constants.DEFAULT_GRPC_PORT)
        default_url = os.environ.get("BLOWPIPE_URL") or default_url
        default_value = default_url.split(":")[1]
        blowpipe_url = os.getenv("BLOWPIPE_PORT", default_value)
        return int(self.data.get("grpc", "port", default_value))

    def set_grpc_port(self, port):
        self.data.set("grpc", "port", port)

    def get_grpc_client_ip(self):
        default_url = constants.DEFAULT_GRPC_SERVER_IP + ":" + str(constants.DEFAULT_GRPC_PORT)
        default_url = os.environ.get("BLOWPIPE_URL") or default_url
        default_value = default_url.split(":")[0]
        return self.data.get("grpc", "client_ip", default_value)

    def set_grpc_client_ip(self, ip):
        self.data.set("grpc", "client_ip", ip)

    def get_grpc_server_ip(self):
        default_url = constants.DEFAULT_GRPC_SERVER_IP + ":" + str(constants.DEFAULT_GRPC_PORT)
        default_url = os.environ.get("BLOWPIPE_URL") or default_url
        default_value = default_url.split(":")[0]
        return self.data.get("grpc", "ip", default_value)

    def set_grpc_server_ip(self, ip):
        self.data.set("grpc", "ip", ip)

    def get_http_port(self):
        return int(self.data.get("http", "port", constants.DEFAULT_HTTP_PORT))

    def set_http_port(self, port):
        self.data.set("http", "port", port)

    def get_http_ip(self):
        return self.data.get("http", "ip", "0.0.0.0")

    def set_http_ip(self, ip):
        self.data.set("http", "ip", ip)

    def get_filename(self):
        return self.filename

    def get_root_dir(self):
        return self.root_dir

    def get_log_dir(self):
        root_dir = self.get_root_dir()
        return root_dir + "/logs"

    def get_syslog_filename(self):
        return self.get_log_dir() + "/syslog.log"


class BlowpipeClientConfig(BlowpipeConfig):
    def __init__(self, filename=None):
        super(BlowpipeClientConfig, self).__init__(filename)

    def set_context(self, context):
        self.data["context"] = context

    def get_context(self):
        return self.data.get("context") or "default"


class BlowpipeServerConfig(BlowpipeConfig):
    def __init__(self, filename=None):
        super(BlowpipeServerConfig, self).__init__(filename)
        self.is_repository = False
