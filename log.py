# !/usr/bin/env python
# --------------------------------------------------------------
# File:          log.py
# Project:       FDU_Timetable
# Created:       Wednesday, 13th November 2019 11:55:35 pm
# @Author:       Molin Liu, MSc in Data Science
# Contact:          molin@live.cn
# Last Modified: Wednesday, 13th November 2019 11:55:38 pm
# Copyright  © Rockface 2019 - 2020
# --------------------------------------------------------------
import os
import datetime
import logging


class LogConfig:
    def __init__(self, log_type="console"):
        if log_type == "console":
            logging.basicConfig(level=logging.INFO,
                                format='%(asctime)s %(levelname)s %(message)s',
                                datefmt='%Y-%m-%d %H:%M:%S',
                                )
        elif log_type == "file":
            if not os.path.exists('./log'):
                os.mkdir('./log')
            nowTime = datetime.datetime.now().strftime('%Y-%m-%d')

            file_name = f'./log/{nowTime}.log'
            file_handler = logging.FileHandler(
                filename=file_name, encoding='utf-8', mode='a')
            # level----指定打印的日志等级；默认为WARNING；可为NOTSET、DEBUG、INFO、WARNING、ERROR、CRITICAL
            # format----指定整条日志的格式；这里设置为“时间-等级-日志内容”
            # datefmt----format中时间的格式；
            # filename----日志输出到的文件；默认打印到控制台
            # filemode----日志文件读写形式；默认为“a”；配合filename使用，如果不用filename该参数也可不用
            # 本来输出到文件使用filename和filemode两个参数就可以了，不需要handlers
            # 但是logging将日志输出到文件时中文会乱码，而logging.basicConfig又没有提供指定编码的参数，要指定编码只能使用handlers
            logging.basicConfig(level=logging.INFO,
                                format='%(asctime)s %(levelname)s %(message)s',
                                datefmt='%Y-%m-%d %H:%M:%S',
                                # filename=file_name,
                                # filemode='a',
                                handlers=[file_handler],
                                )

    def getLogger(self):
        logger = logging.getLogger()
        return logger


if __name__ == "__main__":
    # log_type = "console"
    log_type = "file"
    logger = LogConfig(log_type).getLogger()
    logger.debug('print by debug')
    logger.info('print by info')
    logger.warning('prit by warning')
