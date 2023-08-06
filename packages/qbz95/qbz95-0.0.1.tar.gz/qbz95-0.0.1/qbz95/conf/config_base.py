import logging
import os


logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s')
logging.root.setLevel(level=logging.WARNING)
logging.logThreads = False
logging.logProcesses = False


class ConfigBase():
    def __init__(self, env):
        self.env = env

    package_path = lambda self: None
    data_path = lambda self: None
    base_path = lambda self: os.path.join(self.package_path(), 'arsenal')

    http_proxy = lambda self: None


