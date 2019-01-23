# -*- coding:utf-8 -*-
'''
__author__ = 'XD'
__mtime__ = 2019/1/13
__project__ = 教学评估解析
Fix the Problem, Not the Blame.
'''
import hashlib
from functools import reduce

import requests
import json
import pprint
import re
import random
from operator import itemgetter  # itemgetter用来去dict中的key，省去了使用lambda函数
from itertools import groupby  # itertool还包含有其他很多函数，比如将多个list联合起来


class Stu():

    def __init__(self, num):
        login = self.__get_login(num)  # 获取登陆信息
        self.num = num  # 学号
        self.__token = login['data']['token']  # token信息
        self.name = login['data']['name']  # name
        self.grade = self.__get_grade(self.__token)

    @staticmethod
    def __get_login(student_num, proxy={'https': 'https://119.101.114.103'}):
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

    @staticmethod
    def __get_grade(token):
        '''
        获取成绩信息
        :param token: token参数
        :return:
        '''
        header = {'Content-Type': 'application/json; charset=utf-8',
                  'User-Agent': 'okhttp/3.3.1'
                  }
        url = 'http://42.244.42.160//university-facade/MyUniversity/MyGrades?token={}'.format(token)
        response = requests.get(url, headers=header)
        # 获取具体的成绩列表
        res = json.loads(response.text)['data']  # 得到按学期分的列表
        res = [i['items'] for i in res]  # 得到一个学期的成绩列表
        res = reduce(lambda x, y: x + y, res)  # 扁平化数组
        # 重写构建学期编号
        for i in res:
            i['xq'] = i['xn'][2: 4] + '0{}'.format(i['xq'])
        return res

    @staticmethod
    def __g(point):
        '''
        获取分数对于的G点
        :param point: 分数
        :return: G点
        '''
        point = int(point)
        gpadb = {100: 4.0, 79: 3.2,
                 99: 4.0, 78: 3.1,
                 98: 4.0, 77: 3.0,
                 97: 4.0, 76: 2.9,
                 96: 4.0, 75: 2.8,
                 95: 4.0, 74: 2.7,
                 94: 3.9, 73: 2.6,
                 93: 3.9, 72: 2.5,
                 92: 3.9, 71: 2.4,
                 91: 3.8, 70: 2.3,
                 90: 3.8, 69: 2.2,
                 89: 3.8, 68: 2.1,
                 88: 3.7, 67: 2.0,
                 87: 3.7, 66: 1.8,
                 86: 3.6, 65: 1.7,
                 85: 3.6, 64: 1.6,
                 84: 3.5, 63: 1.4,
                 83: 3.5, 62: 1.3,
                 82: 3.4, 61: 1.1,
                 81: 3.3, 60: 1.0,
                 80: 3.3}
        if point < 60:
            return 0
        else:
            return gpadb[point]

    def __get_token(self, student_num, proxy={'https': 'https://119.101.114.103'}):
        '''
        当login失效时，或者想单独获取token信息，用来登陆。
        :param student_num: 学号
        :param proxy: 单个代理
        :return: token信息
        '''
        login_content = self.__get_login(student_num, proxy)
        token_text = login_content['data']['token']
        return token_text

    def get_GPA(self):
        '''
        获取GPA，所有的，每个学期的。
        :return:
                {'all': ~,
                'xq': {
                        '1801':~,
                        '1802':~,
                        ...
                    }
                }
        '''

        def get_G(grade):
            effectiv_grade = list(filter(lambda x: x['cj'].isdigit(), grade))  # 去除所有等级
            xf = 0  # 总学分
            G = 0
            for i in effectiv_grade:
                xf += int(i['xf'])
                G += int(i['xf']) * self.__g(i['cj'])
            G = '{:.2f}'.format(G / xf)  # 保留两位小数
            return float(G)

        res = {}  # 储存结果
        # 总绩点
        G = get_G(self.grade)  # 保留两位小数
        res['0000'] = G
        # xq分组
        xq = groupby(self.grade, itemgetter('xq'))
        for i in xq:
            res[i[0]] = get_G(i[1])
        return res


a = Stu('1809401020')
print(a.num, a.name)
print(a.get_GPA())
