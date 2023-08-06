import json
import logging
import os
import signal
import sys

from ..package_manager import package_manager
from .rpc import RuntimeRpc

logger = None
config = None
rpc = None


class RuntimeLoggingHandler(logging.StreamHandler):

    def __init__(self, rpc, identity):
        self.rpc = rpc
        self.identity = identity
        super().__init__()

    def emit(self, record):
        self.rpc.log(record)


def init_config(config_file=None):
    global config
    with open(config_file if config_file else './config.json', 'r') as f:
        config = json.loads(f.read())


def init_logger():
    global logger
    logging_format = '%(levelname)s %(asctime)s %(message)s'
    logging.basicConfig(
        format=logging_format,
        datefmt="%m-%d %H:%M:%S",
        level=logging.INFO
    )

    logger = logging.getLogger(f'runtime{os.getpid()}')
    handler = RuntimeLoggingHandler(rpc, config.get('identity'))
    handler.setLevel(logging.INFO)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)


def init_rpc():
    global rpc
    if rpc is not None:
        # if rpc is not None, then the rpc is a forked version
        # we need to close the channel first otherwise it will
        # failed the first call 100%
        rpc.channel.close()
    rpc = RuntimeRpc(config['server_addr'], config['identity'])

    def graceful_shutdown(signum, frame):
        rpc.executor.shutdown()
        sys.exit(0)

    signal.signal(signal.SIGTERM, graceful_shutdown)


def init_packages():
    global config
    for package_name in config['enabled_package']:
        package_manager.add_package(package_name)


def init_process_env(config_file=None):
    init_config(config_file)
    init_rpc()
    init_logger()
    init_packages()
