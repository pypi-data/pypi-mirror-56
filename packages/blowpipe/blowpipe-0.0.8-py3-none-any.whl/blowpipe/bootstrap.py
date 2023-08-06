import os
import sys
from common import utils
from common.ini import IniFile
from common.cli import CLI
import concurrent.futures
from blowpipe.logger import Logger
from blowpipe import config
from blowpipe import constants
from blowpipe import model_db
from blowpipe.server import BlowpipeServerConfig
from blowpipe.exceptions import BlowpipeError

DEFAULT_CONFIG_FILE = utils.resolve_file("~/.blowpipe/blowpipe.cfg")
DEFAULT_DIR = utils.resolve_file("~/.blowpipe")


def autodiscover_config_file() -> (str, int):
    """
    finds the appropriate filename in the following order
    - cli -f argument
    - environment variable
    - current dir
    returns a tuple (filename, style) 1, 2, 3 cfg, sys var, current dir
    """
    cli = CLI(sys.argv)
    cfg_filename = cli.get_or_default("-config", None)
    if cfg_filename is not None:
        return utils.resolve_file(cfg_filename)
    else:
        env_root_dir = os.getenv("BLOWPIPE_HOME")
        if env_root_dir is None or env_root_dir.strip() == "":
            print("autodiscover_config_file: using default " + DEFAULT_DIR)
            env_root_dir = DEFAULT_DIR
        else:
            print("autodiscover_config_file: using env BLOWPIPE_HOME " + env_root_dir)

        env_file = utils.resolve_file(env_root_dir + "/blowpipe.cfg")
        return env_file


def init(filename: str) -> BlowpipeServerConfig:
    """
    Initialises
        - blowpipe.cfg file pointed to by filename
        - sqlite database as a sibling file 'blowpipe.db'
        - folder for logs

    this includes
        blowpipe.cfg
        blowpipe.db
        logs/
    :param filename: a path to a blowpipe.cfg file, e..g /Users/YOU/blowpipe/blowpipe.cfg
    :return:
    """

    if os.path.isfile(filename):
        raise BlowpipeError("Already exists.")

    abs_filename = utils.resolve_file(filename)
    parent_dir, fname = utils.split_file(abs_filename)
    if not os.path.isdir(parent_dir):
        os.makedirs(parent_dir)

    content = constants.DEFAULT_CONFIG
    content = content.replace("TOKEN_HTTP_PORT", str(constants.DEFAULT_HTTP_PORT))
    content = content.replace("TOKEN_GRPC_PORT", str(constants.DEFAULT_GRPC_PORT))
    content = content.replace(
        "TOKEN_GRPC_CLIENT_IP", str(constants.DEFAULT_GRPC_CLIENT_IP)
    )
    content = content.replace(
        "TOKEN_GRPC_SERVER_IP", str(constants.DEFAULT_GRPC_SERVER_IP)
    )

    Logger.console("Initialising '" + filename + "'.")
    f = open(abs_filename, "w")
    f.write(content)
    f.close()

    cfg = IniFile(abs_filename)
    if not os.path.isdir(cfg.get_root_dir()):
        os.makedirs(cfg.get_root_dir())

    Logger.console("Initialising '" + filename + "' ok.")

    log_dirname = cfg.get_root_dir() + "/logs"
    if not os.path.isdir(log_dirname):
        os.makedirs(log_dirname)

    sqlite_filename = "sqlite:///" + cfg.get_root_dir() + "/blowpipe.db"
    db = model_db.DB(cfg, sqlite_filename)
    db.connect()
    db.reset()
    cfg.save()

    Logger.console("Initialised Blowpipe in " + cfg.get_root_dir())
    config = BlowpipeServerConfig(filename)
    return config


def init_temporary() -> BlowpipeServerConfig:
    """
    creates a temp dir bootstrap file
    :param self:
    :return:
    """
    blowpipe_home = utils.resolve_file("${TMPDIR}/blowpipe/")
    f = blowpipe_home + "/blowpipe.cfg"
    return init(f)
