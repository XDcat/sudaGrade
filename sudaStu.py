# -*- coding:utf-8 -*-
'''
__author__ = 'XD'
__mtime__ = 2019/1/13
__project__ = 教学评估解析
Fix the Problem, Not the Blame.
'''
import hashlib
import requests
import json
import pprint
import re
import random


class SudaStu():

    def __init__(self, num):
        login = self.__get_login(num)  # 获取登陆信息
        self.num = num  # 学号
        self.__token = login['data']['token']  # token
        self.name = login['data']['name']  # name

    def __get_login(self, student_num, proxy={'https': 'https://119.101.114.103'}):
        '''
        获取动态的token
        :param student_num: 学号
        :param proxy: 单个代理
        :return: str
        '''
        # mod5加密, 传入头
        p_text = hashlib.md5(student_num.encode('utf-8')).hexdigest()
        # 头信息
        header = {'Content-Type': 'application/json; charset=utf-8',
                  'User-Agent': 'okhttp/3.3.1'
                  }
        # data
        data = {
            "u": student_num,
            "p": p_text
        }
        # url
        url = 'http://42.244.42.160/university-facade/Murp/Login'
        # 请求
        response = requests.post(url, data=json.dumps(data), headers=header, proxies=proxy, timeout=6)
        return json.loads(response.text)

    def __get_token(self, student_num, proxy={'https': 'https://119.101.114.103'}):
        '''
        获取token信息，用来登陆。
        :param student_num: 学号
        :param proxy: 单个代理
        :return: token信息
        '''
        login_content = self.__get_login(student_num, proxy)
        token_text = login_content['data']['token']
        return token_text


a = SudaStu('1709404008')
print(a.num, a.name)
