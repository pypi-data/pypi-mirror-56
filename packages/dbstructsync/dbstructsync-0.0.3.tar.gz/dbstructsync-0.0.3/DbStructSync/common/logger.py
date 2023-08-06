#-*-coding:utf-8-*-
import  logging

import logging.config
import os
import threading

import yaml


class Logger(object):
    """
    功能: 日志单例类
    保证在项目中仅创建一个日志类，并配置日志的输出格式，输出地址
    由于项目日志不会太多，先暂时只允许输出到一个文件里

    author='liuyingchen'
    调用方法：
    from utils.Logger import Logger
    logger = Logger()
    logger.error
    logger.info
    logger.debug

    """
    # 线程锁
    __instance_lock = threading.Lock()

    def __init__(self):
        pass

    def __new__(cls, *args, **kwargs):

        if not hasattr(Logger, '_instance'):
            with Logger.__instance_lock:
                if not hasattr(Logger, '_instance'):
                    Logger._instance = object.__new__(cls, *args)
                    value = os.getenv('LOG_CFG', None)
                    if value:
                        path = value
                    else:
                        path = os.path.join(os.path.dirname(__file__), 'logging.yaml')
                    if os.path.exists(path):
                        with open(path, 'r') as f:
                            config_dict = yaml.load(f)
                            path = os.path.dirname(__file__)
                            log_dir = os.path.join(os.path.dirname(path), 'log')
                            if not os.path.exists(log_dir):
                                os.makedirs(log_dir)
                                print('log文件夹不存在，已新建成功')
                            config_dict['handlers']['info_file_handler']['filename'] = os.path.join(log_dir,
                                                                                                    'console.log')
                            logging.config.dictConfig(config_dict)
                    else:
                        logging.basicConfig(level=logging.INFO)
                    logger = logging.getLogger('fileLogger')
                    Logger._instance = logger

        return Logger._instance
