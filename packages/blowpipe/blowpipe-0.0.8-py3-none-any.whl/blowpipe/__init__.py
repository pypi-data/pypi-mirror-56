import os
import sys
from blowpipe.client_cli import BlowpipeClient
from blowpipe.config import BlowpipeClientConfig, BlowpipeServerConfig
from blowpipe.server import BlowpipeServer
from common import utils
from common.cli import CLI
import blowpipe
from blowpipe import constants
from blowpipe.logger import Logger
from blowpipe import bootstrap
from blowpipe import bp_utils


def server(cli: CLI):
    filename = bootstrap.autodiscover_config_file()
    if not os.path.isfile(filename):
        msg = (
            "Error, Blowpipe server cannot run, no configuration found."
            + "\nYou must set one of the following:"
            + "\n"
            + "\n\t1. $BLOWPIPE_HOME"
            + "\n\t2. 'blowpipe.cfg' not found in current dir."
            + "\n\t3. Pass location of config file with '-config' option."
            + "\n"
        )
        Logger.console(msg)
        sys.exit(1)

    cfg = BlowpipeServerConfig(filename)
    cfg.is_repository = cli.contains("-repository")

    grpc_ip = cfg.get_grpc_server_ip()
    if grpc_ip == "::":
        grpc_ip = "127.0.0.1"

    if not utils.is_port_available(grpc_ip, cfg.get_grpc_port()):
        # looks like something is running on that port.
        # let's see if we can connect to it as the client; if we can
        # then we will be
        if bp_utils.is_server_running(cfg):
            friendly = cfg.get_grpc_server_ip() + ":" + str(cfg.get_grpc_port())
            print("Error, Blowpipe Server is already running on " + friendly)
        else:
            print(
                "Error, port "
                + str(cfg.get_grpc_port())
                + " already in use by something else."
            )
        sys.exit(1)
    else:
        bp_utils.print_logo()
        srv = BlowpipeServer(cfg)
        srv.start(blocking=True)


def client(cli: CLI):
    filename = bootstrap.autodiscover_config_file()
    default_filename = utils.resolve_file("~/.blowpipe/blowpipe.cfg")
    if not os.path.isfile(filename):
        if not os.path.isfile(default_filename):
            if blowpipe.constants.VERBOSE:
                Logger.console(
                    "No configuration file found - using default client settings."
                )
            cfg = BlowpipeClientConfig()
        else:
            filename = default_filename
            cfg = BlowpipeClientConfig(filename)
    else:
        cfg = BlowpipeClientConfig(filename)

    default_server = cfg.get_grpc_client_ip() + ":" + str(cfg.get_grpc_port())
    server_url = os.getenv("BLOWPIPE_URL", default_server)
    splits = server_url.split(":")
    hostname = splits[0]
    port = splits[1]

    cfg.set_grpc_server_ip(hostname)
    cfg.set_grpc_port(port)

    cli = bp_utils.CLI()
    myclient = BlowpipeClient(cfg)
    myclient.process(cli)


def main():
    cli = CLI(sys.argv)
    blowpipe.logger.CONSOLE_ENABLED = cli.contains("-v")
    blowpipe.constants.VERBOSE = cli.contains("-v")
    if cli.get_command() == "server":
        server(cli)
    else:
        client(cli)
