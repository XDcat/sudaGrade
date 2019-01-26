# -*- coding:utf-8 -*-
"""
__author__ = 'XD'
__mtime__ = 2019/1/13
__project__ = 教学评估解析
Fix the Problem, Not the Blame.
"""
import hashlib
import sqlite3
import sys
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
from db import db

logger = Logger().logger


class Stu:
    """
    主要的属性：
    num: 学号
    name: 姓名
    grade: 成绩的字典
    GPA: 总G点
    info: 个人信息
    """

    def __init__(self, num, password=None):
        # 初始化值
        self.num = num  # 学号
        self.name = self.score = self.GPA = self.info = None
        # 选择从数据库查询还是在线查询
        self.isInDB = db.has_num(num)
        if self.isInDB:
            if self.isInDB['isLogable'] != 1:
                logger.info('[%s]在数据库中：无信息。', num)
                pass
            else:
                self.name = self.isInDB['name']
                self.score = json.loads(self.isInDB['score'])
                self.GPA = self.isInDB['GPA']
                self.info = json.loads(self.isInDB['info'])
                logger.info('[%s]在数据库中：%s-%s', num, self.name, self.GPA)
        else:
            login = self.__get_login(num, password)  # 获取登陆信息
            # 判断是否可以爬取
            if login:
                # 保存详细数据
                self.__token = login['data']['token']  # token信息
                self.name = login['data']['name']  # name
                self.score = self.__get_grade(num, self.__token)
                self.GPA = self.get_GPA()['0000']
                self.info = self.__person_info(self.__token)
                db.insert_stu(self.num, 1, self.__token, self.name, self.score, self.GPA, self.info)
                logger.info('[%s]不在在数据库中，正常爬取：%s-%s', num, self.name, self.GPA)
            else:
                self.__token = self.name = self.score = None
                db.insert_stu(self.num, 0, self.__token, self.name, self.score, self.GPA, self.info)
                logger.info('[%s]不在在数据库中，无法爬取：%s-%s', num, self.name, self.GPA)

    @staticmethod
    def __get_login(student_num, password):
        """
        获取动态的token
        :param student_num: 学号
        :param proxy: 单个代理
        :return: 如果成功登陆返回登陆信息字典；否则密码错误，返回None；
        """
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
        response = StuTools.requests_post(url, data=json.dumps(data), headers=header, timeout=3)
        res = json.loads(response.text)
        if res['state'] == 2002:
            return None
        else:
            return res

    @staticmethod
    def __get_grade(num, token):
        """
        获取成绩信息
        :param token: token参数
        :return:
        """
        header = {'Content-Type': 'application/json; charset=utf-8',
                  'User-Agent': 'okhttp/3.3.1'
                  }
        url = 'http://42.244.42.160//university-facade/MyUniversity/MyGrades?token={}'.format(token)
        response = StuTools.requests_get(url, headers=header)
        res = json.loads(response.text)
        # 如果未完成教学评价，帮助其完成
        if res['state'] == 4001:
            Stu.__jxpg(num, token)
            response = StuTools.requests_get(url, headers=header)
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
        """
        获取分数对于的G点
        :param point: 分数
        :return: G点
        """
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

    def __get_token(self, student_num, password):
        """
        当login失效时，或者想单独获取token信息，用来登陆。
        :param student_num: 学号
        :param proxy: 单个代理
        :return: token信息
        """
        login_content = self.__get_login(student_num, password)
        token_text = login_content['data']['token']
        return token_text

    @staticmethod
    def __jxpg(num, token):
        """完成教学评估"""
        header = {'Content-Type': 'application/json; charset=utf-8',
                  'User-Agent': 'okhttp/3.3.1'
                  }
        # 获取待评测列表
        url = 'http://42.244.42.160/university-facade/TeachingEvaluation/queryWaitList.shtml?token={}&pageIndex=0&pageSize=10000'.format(
            token)
        response = StuTools.requests_get(url, headers=header)
        classes = json.loads(response.text)['data']['rows']
        classes = [i['id'] for i in classes]  # 得到带评测课程的id
        # 评测
        for aclass in classes:
            # 获取评测界面
            url = 'http://42.244.42.160/university-facade//TeachingEvaluation/queryPaperForWait.shtml?id={}&token={}'.format(
                aclass, token)
            response = StuTools.requests_get(url, headers=header)
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
            response = requests.post(url, data=data, headers=header)
            response = json.loads(response.text)
            if response['state'] != 200:
                raise Exception('出错:'.format(response))

    @staticmethod
    def __person_info(token):
        """获取个人信息列表"""
        header = {'Content-Type': 'application/json; charset=utf-8',
                  'User-Agent': 'okhttp/3.3.1'
                  }
        # 获取待评测列表
        url = 'http://42.244.42.160/university-facade/MyUniversity/StudyState?token={}&suno=null'.format(
            token)
        response = StuTools.requests_get(url, headers=header)
        info = json.loads(response.text)['data']
        res = {}
        for i in info:
            res[i['k']] = i['v']
        return res

    def get_GPA(self):
        """
        获取GPA，所有的，每个学期的。
        :return: GPA的字典
        """

        def get_G(grade):
            effectiv_grade = list(filter(lambda x: x['cj'].isdigit(), grade))  # 去除所有等级
            xf = 0  # 总学分
            G = 0
            for i in effectiv_grade:
                xf += int(i['xf'])
                G += int(i['xf']) * self.__g(i['cj'])
            G = '{:.2f}'.format(G / xf)  # 保留两位小数
            return float(G)

        grade = self.score
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
        """
        查找各个专业对应的学号, 即学号的前缀
        e.g. 1709404001 => 1709404
        :param grade: 年纪
        :return:None
        """
        academy = db.select_all('academy')
        for aAcademy in academy:
            # 遍历每一个学号
            # 学号 = 年级 + 学院 + 专业 + 编号
            # e.g. 17 + 01 + 401 + 001
            # 专业
            for i in range(10):
                for j in range(10):
                    for k in range(10):
                        # 编号：可能出现改密码的情况所以重复三个
                        for l in range(1, 4):
                            num = '{}{}{}{}{}00{}'.format(grade, aAcademy['id'], i, j, k, l)
                            logger.info('尝试获取所有{}级专业, 尝试: {}'.format(grade, num))
                            astu = Stu(num)
                            if astu.name:
                                # 如果成功获取保存数据
                                db.insert_major(num[:-3], grade, astu.info['学院'], astu.info['专业'])
                                logger.info('成功找到专业: %s', num)
                                break
                            else:
                                logger.info('无法找到专业: %s', num)

    @staticmethod
    def requests_post(url, data, headers, timeout=3):
        """单独封装的post，可以重试10次"""
        count = 0
        while True:
            try:
                res = requests.post(url, data=data, headers=headers, proxies=StuTools.get_proxy(), timeout=timeout)
                return res
            except:
                count += 1
                logger.error('POST失败, 即将重试第%s次。', count, exc_info=True)

    @staticmethod
    def requests_get(url, headers, timeout=3):
        """单独封装的get，可以重试10次"""
        count = 0
        while True:
            try:
                res = requests.get(url, headers=headers, proxies=StuTools.get_proxy(), timeout=timeout)
                return res
            except:
                count += 1
                logger.error('GET失败, 即将重试第%s次。', count, exc_info=True)

    @staticmethod
    def get_proxy():
        proxies = [{'https': 'http://171.12.112.33:9999'},
                   {'http': 'http://59.56.168.140:9999'},
                   {'http': 'http://110.52.235.251:9999'},
                   {'http': 'http://114.106.135.157:9999'},
                   {'https': 'http://61.145.69.27:42380'},
                   {'http': 'http://121.61.1.196:9999'},
                   {'http': 'http://121.61.0.14:9999'},
                   {'https': 'http://111.181.36.202:9999'},
                   {'https': 'http://222.217.30.8:9999'},
                   {'https': 'http://115.151.1.11:808'},
                   {'http': 'http://110.83.40.16:9999'},
                   {'http': 'http://119.102.24.182:9999'},
                   {'https': 'http://119.102.25.222:9999'},
                   {'http': 'http://111.181.38.9:9999'},
                   {'http': 'http://119.102.27.51:9999'},
                   {'https': 'http://121.61.1.180:9999'},
                   {'http': 'http://119.102.25.83:9999'},
                   {'http': 'http://119.102.26.128:9999'},
                   {'http': 'http://125.126.211.49:9999'},
                   {'http': 'http://218.85.22.152:9999'},
                   {'http': 'http://111.176.29.214:9999'},
                   {'http': 'http://114.239.151.132:808'},
                   {'https': 'http://125.119.55.2:9999'},
                   {'http': 'http://222.217.30.98:9999'},
                   {'http': 'http://218.85.22.52:9999'},
                   {'http': 'http://183.148.131.5:9999'},
                   {'http': 'http://110.83.40.102:9999'},
                   {'https': 'http://223.241.116.249:8010'},
                   {'https': 'http://110.83.40.93:9999'},
                   {'https': 'http://27.29.76.151:9999'},
                   {'http': 'http://115.151.5.162:9999'},
                   {'http': 'http://27.156.119.171:9999'},
                   {'http': 'http://111.181.36.235:9999'},
                   {'http': 'http://27.156.119.91:9999'},
                   {'http': 'http://121.61.1.213:9999'},
                   {'http': 'http://110.83.40.223:9999'},
                   {'http': 'http://110.83.40.42:9999'},
                   {'http': 'http://117.28.218.162:8118'},
                   {'http': 'http://223.241.119.133:8010'},
                   {'https': 'http://113.120.63.221:9999'},
                   {'https': 'http://183.148.159.110:9999'},
                   {'http': 'http://114.225.220.98:9999'},
                   {'http': 'http://218.85.22.102:9999'},
                   {'http': 'http://110.83.40.18:9999'},
                   {'https': 'http://183.148.155.80:9999'},
                   {'https': 'http://112.85.131.7:9999'},
                   {'https': 'http://61.189.242.243:55484'},
                   {'https': 'http://223.153.229.216:9999'},
                   {'https': 'http://123.244.148.19:52168'},
                   {'http': 'http://121.61.0.127:9999'},
                   {'http': 'http://115.151.4.84:9999'},
                   {'http': 'http://115.151.0.164:9999'},
                   {'http': 'http://116.209.57.154:9999'},
                   {'https': 'http://171.41.85.218:9999'},
                   {'https': 'http://115.151.6.90:808'},
                   {'https': 'http://123.180.68.25:9999'},
                   {'http': 'http://115.151.7.142:9999'},
                   {'http': 'http://59.56.168.224:9999'},
                   {'http': 'http://125.123.139.152:9999'},
                   {'https': 'http://218.85.22.28:9999'},
                   {'https': 'http://115.151.3.78:808'},
                   {'https': 'http://125.123.142.158:9999'},
                   {'https': 'http://115.151.3.179:9999'},
                   {'https': 'http://121.61.1.55:9999'},
                   {'http': 'http://121.61.1.145:9999'},
                   {'http': 'http://121.61.2.1:9999'},
                   {'http': 'http://59.56.168.24:9999'},
                   {'http': 'http://121.61.0.24:9999'},
                   {'http': 'http://111.181.69.205:9999'},
                   {'https': 'http://122.194.139.153:9999'},
                   {'https': 'http://111.181.69.163:9999'},
                   {'https': 'http://58.55.148.140:9999'},
                   {'https': 'http://171.41.83.38:9999'},
                   {'http': 'http://115.151.0.178:9999'},
                   {'http': 'http://171.41.82.94:9999'},
                   {'http': 'http://121.61.2.115:9999'},
                   {'http': 'http://113.13.177.143:9999'},
                   {'https': 'http://58.55.148.103:9999'},
                   {'https': 'http://115.151.6.89:9999'},
                   {'https': 'http://171.41.81.148:9999'},
                   {'https': 'http://117.91.249.29:9999'},
                   {'https': 'http://218.85.22.244:9999'},
                   {'https': 'http://1.192.241.250:9999'},
                   {'https': 'http://171.41.82.251:9999'},
                   {'https': 'http://110.52.235.107:9999'},
                   {'https': 'http://115.151.4.195:9999'},
                   {'https': 'http://115.46.98.212:8123'},
                   {'http': 'http://111.181.66.193:9999'},
                   {'http': 'http://115.151.3.239:9999'},
                   {'http': 'http://117.95.198.62:9999'},
                   {'http': 'http://115.151.1.10:9999'},
                   {'https': 'http://218.85.22.166:9999'},
                   {'https': 'http://27.156.119.8:9999'},
                   {'https': 'http://110.52.235.92:9999'},
                   {'https': 'http://113.7.191.55:8118'},
                   {'https': 'http://61.142.72.150:39894'},
                   {'http': 'http://117.85.49.35:9999'},
                   {'http': 'http://171.211.27.73:9999'},
                   {'https': 'http://27.156.119.246:9999'},
                   {'http': 'http://121.61.2.69:9999'}]
        return random.choice(proxies)


# print(db.has_num('1898798'))
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

# 数据从14级开始
if __name__ == '__main__':
    input_argv = sys.argv
    StuTools.get_major_stu_num(input_argv[1])
    # a = Stu('1609404010')
