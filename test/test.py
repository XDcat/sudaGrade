# -*- coding:utf-8 -*-
'''
__author__ = 'XD'
__mtime__ = 2019/1/24
__project__ = 教学评估解析
Fix the Problem, Not the Blame.
'''
import json
import re
from pprint import pprint

import requests


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
        response = json.loads(response)
        if response['state'] != 200:
            raise Exception('出错:'.format(response))


if __name__ == '__main__':
    __jxpg('1709404028', '09d278449c42466ca168ee6f98160448')
