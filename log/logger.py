# -*- coding:utf-8 -*-
'''
__author__ = 'XD'
__mtime__ = 2019/1/25
__project__ = 教学评估解析
Fix the Problem, Not the Blame.
'''
import logging
import os
import logging.config
import yaml


class Logger:
    '''根据配置文件生成logger'''
    def __init__(self, default_path='log/conf.yaml', default_level=logging.INFO):
        path = default_path
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                config = yaml.load(f)
                logging.config.dictConfig(config)
        else:
            logging.basicConfig(level=default_level)
        self.logger = logging.getLogger('main.core')