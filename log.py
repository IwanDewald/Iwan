# log.py
# !/usr/bin/venv python
# -*- coding: utf-8 -*-

import logging

import config
import constants

logging.basicConfig(format=u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.INFO, filename=config.log)


def making_logs(log_message):
    with open(config.log, 'r+') as f:
        f.write(constants.delimeter)
        if type(log_message) == Exception:
            logging.exception('\n' + str(log_message) + '\n')
        else:
            logging.info('\n' + str(log_message) + '\n')
