# -*- coding:utf-8 -*-
'''
__author__ = 'XD'
__mtime__ = 2019/1/13
__project__ = 教学评估解析
Fix the Problem, Not the Blame.
'''
import hashlib
import sqlite3
import traceback
from functools import reduce

import requests
import json
import pprint
import re
import random
from operator import itemgetter  # itemgetter用来去dict中的key，省去了使用lambda函数
from itertools import groupby  # itertool还包含有其他很多函数，比如将多个list联合起来
from log.logger import Logger

logger = Logger().logger


class Stu:
    '''
    主要的属性：
    num: 学号
    name: 姓名
    grade: 成绩的字典
    GPA: 总G点
    '''

    def __init__(self, num, password=None):
        # 初始化值
        self.num = num  # 学号
        self.name = self.grade = self.GPA = None
        # 选择从数据库查询还是在线查询
        self.isInDB = StuTools.db_has_num(num)
        if self.isInDB:
            if self.isInDB['isLogable'] != 1:
                pass
            else:
                self.name = self.isInDB['name']
                self.grade = json.loads(self.isInDB['grade'])
                self.GPA = self.isInDB['GPA']
        else:
            login = self.__get_login(num, password)  # 获取登陆信息
            # 判断是否可以爬取
            if login:
                # 保存详细数据
                self.__token = login['data']['token']  # token信息
                self.name = login['data']['name']  # name
                self.grade = self.__get_grade(num, self.__token)
                self.GPA = self.get_GPA()['0000']
                StuTools.db_insert(self.num, 1, self.__token, self.name, self.grade, self.GPA)
            else:
                self.__token = self.name = self.grade = None
                StuTools.db_insert(self.num, 0, '', '', '', '')

    @staticmethod
    def __get_login(student_num, password, proxy={'https': 'https://119.101.114.103'}):
        '''
        获取动态的token
        :param student_num: 学号
        :param proxy: 单个代理
        :return: 如果成功登陆返回登陆信息字典；否则密码错误，返回None；
        '''
        # mod5加密, 传入头
        if password:
            p_text = hashlib.md5(password.encode('utf-8')).hexdigest()
        else:
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
        res = json.loads(response.text)
        if res['state'] == 2002:
            return None
        else:
            return res

    @staticmethod
    def __get_grade(num, token, proxy={'https': 'https://119.101.114.103'}):
        '''
        获取成绩信息
        :param token: token参数
        :return:
        '''
        header = {'Content-Type': 'application/json; charset=utf-8',
                  'User-Agent': 'okhttp/3.3.1'
                  }
        url = 'http://42.244.42.160//university-facade/MyUniversity/MyGrades?token={}'.format(token)
        response = requests.get(url, headers=header, proxies=proxy)
        res = json.loads(response.text)
        # 如果未完成教学评价，帮助其完成
        if res['state'] == 4001:
            Stu.__jxpg(num, token)
            response = requests.get(url, headers=header, proxies=proxy)
            res = json.loads(response.text)
        # 获取具体的成绩列表
        res = res['data']  # 得到按学期分的列表
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

    def __get_token(self, student_num, password, proxy={'https': 'https://119.101.114.103'}):
        '''
        当login失效时，或者想单独获取token信息，用来登陆。
        :param student_num: 学号
        :param proxy: 单个代理
        :return: token信息
        '''
        login_content = self.__get_login(student_num, password, proxy)
        token_text = login_content['data']['token']
        return token_text

    @staticmethod
    def __jxpg(num, token, proxy={'https': 'https://119.101.114.103'}):
        '''完成教学评估'''
        header = {'Content-Type': 'application/json; charset=utf-8',
                  'User-Agent': 'okhttp/3.3.1'
                  }
        # 获取待评测列表
        url = 'http://42.244.42.160/university-facade/TeachingEvaluation/queryWaitList.shtml?token={}&pageIndex=0&pageSize=10000'.format(
            token)
        response = requests.get(url, headers=header, proxies=proxy)
        classes = json.loads(response.text)['data']['rows']
        classes = [i['id'] for i in classes]  # 得到带评测课程的id
        # 评测
        for aclass in classes:
            # 获取评测界面
            url = 'http://42.244.42.160/university-facade//TeachingEvaluation/queryPaperForWait.shtml?id={}&token={}'.format(
                aclass, token)
            response = requests.get(url, headers=header, proxies=proxy)
            ques = re.findall('"id":"(.*?)"', response.text)  # 问题的id
            ques = ['subjectId:{},type:0,optionSn:1'.format(i) for i in ques]
            # 回答问题
            url = 'http://42.244.42.160/university-facade//TeachingEvaluation/SaveResultDataH5.shtml'
            header = {
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'Cookie': 'userNo={}; app=1; token={}'.format(num, token),
                'Referer': 'http://42.244.42.160/static/html/teaching/course_evaluate_l.html?id=&sutype=null&loadtype=null&isNotice=1'.format(
                    token),
                'X-Requested-With': 'XMLHttpRequest'}
            data = {
                'data': ques,
                'masterid': aclass
            }
            response = requests.post(url, data=data, headers=header, proxies=proxy)
            response = json.loads(response.text)
            if response['state'] != 200:
                raise Exception('出错:'.format(response))

    def get_GPA(self):
        '''
        获取GPA，所有的，每个学期的。
        :return: GPA的字典
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

        grade = self.grade
        grade = [i for i in grade if i['kcxz'] != '其他课程']
        res = {}  # 储存结果
        # 总绩点
        G = get_G(grade)  # 保留两位小数
        res['0000'] = G
        # xq分组
        xq = groupby(grade, itemgetter('xq'))
        for i in xq:
            res[i[0]] = get_G(i[1])
        return res


class StuTools:

    @staticmethod
    def get_major_stu_num(grade):
        '''
        查找各个专业对应的学号, 即学号的前缀
        e.g. 1709404001 => 1709404
        :param grade: 年纪
        :return:None
        '''
        academy = StuTools.db_select_all('academy')
        for aAcademy in academy:
            # 遍历每一个学号
            # 学号 = 年级 + 学院 + 专业 + 编号
            # e.g. 17 + 01 + 401 + 001
            num = grade
            # 专业
            for i in range(10):
                for j in range(10):
                    for k in range(10):
                        # 编号：可能出现改密码的情况所以重复三个
                        for l in range(4):
                            pass

    @staticmethod
    def db_dict_factory(cursor, row):
        '''Cursor的工厂方法：返回字典'''
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

    @staticmethod
    def db_select_all(table):
        '''获取表中所有数据'''
        con = sqlite3.connect('db/sudaStu.db')
        con.row_factory = StuTools.db_dict_factory  # 指定工厂方法
        res = con.execute('SELECT * FROM ?', (table,)).fetchall()
        con.close()
        return res

    @staticmethod
    def db_has_num(num):
        '''数据库中是否存在num学号'''
        con = sqlite3.connect('db/sudaStu.db')
        con.row_factory = StuTools.db_dict_factory  # 指定工厂方法
        res = con.execute('SELECT * FROM stu WHERE stuNum = ?', (num,)).fetchone()
        con.close()
        return res

    @staticmethod
    def db_insert(num, isLogable, token, name, grade, GPA):
        '''
        保存数据
        :param num: 学号
        :param isLogable: 是否可登陆
        :param token: ~
        :param name: 姓名
        :param grade: 成绩
        :return: None
        '''
        con = sqlite3.connect('db/sudaStu.db')
        con.execute('INSERT INTO stu (stuNum, isLogable, token, name, grade, GPA) VALUES (?, ?, ?, ?, ?, ?)',
                    (num, isLogable, token, name, json.dumps(grade), str(GPA)))
        con.commit()
        con.close()


# print(StuTools.db_has_num('1898798'))
# a = Stu('1709404010', 'Zlj1784470039')
# pprint.pprint(a.grade)
# print(a.get_GPA())
# for i in range(1, 144):
#     try:
#         a = Stu('1809404{:03}'.format(i))
#         logger('1709404{:03}'.format(i))
#     except:
#         logger(i)
#         traceback.print_exc()
logger.info('alsdkfj')
# 数据从14级开始
