#!/usr/bin/env python
import logging
import os
from qbz95.conf import config_jupyter
from qbz95 import env

deployment = env.params['deployment']

if deployment == 'jupyter':
    config = config_jupyter.ConfigJupyter()
else:
    raise Exception('wrong deployment')

logging.info('deployment = ' + deployment)
logging.info('base_path = ' + config.base_path())
logging.info('data_path = ' + config.data_path())

if config.http_proxy() is not None:
    os.environ['HTTPS_PROXY'] = config.http_proxy()
    os.environ['HTTP_PROXY'] = config.http_proxy()




