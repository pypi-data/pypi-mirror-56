import logging
import os
from qbz95.conf.config_base import ConfigBase

logging.root.setLevel(level=logging.INFO)

class ConfigJupyter(ConfigBase):

    def __init__(self):
        ConfigBase.__init__(self, 'jupyter')

    package_path = lambda self: '/notebooks/eipi10/arsenal'
    data_path = lambda self: os.path.join(self.package_path(), 'data')

    http_proxy = lambda self: 'http://web-proxy.rose.hp.com:8080'



