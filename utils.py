# !/usr/bin/env python
# --------------------------------------------------------------
# File:          utils.py
# Project:       FDU_Timetable
# Created:       Wednesday, 13th November 2019 11:39:59 am
# @Author:       Molin Liu, MSc in Data Science
# Contact:          molin@live.cn
# Last Modified: Wednesday, 13th November 2019 11:40:01 am
# Copyright  © Rockface 2019 - 2020
# --------------------------------------------------------------

import os
from log import LogConfig

'''
Initialize Logger
'''
logger = LogConfig('console').getLogger()


def parseCookie(value):
    result = {}
    for item in value.split(';'):
        item = item.strip()
        if not item:
            continue
        if '=' not in item:
            result[item] = None
            continue
        name, value = item.split('=', 1)
        result[name] = value
    return result


def saveHtml(title, text, code):
    i = 0
    filename = 'Test_%s_0_%d.html' % (title, code)
    while(os.path.exists(filename)):
        i += 1
        filename = 'Test_%s_%d_%d.html' % (title, i, code)
    with open(filename, 'w') as file:
        file.write(text)
        file.close()
    logger.info("SUCCESS: Save to %s." % filename)
