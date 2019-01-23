# ~/annaconda3/bin/python3.6
# -*- coding:utf-8 -*-
'''
__author__ = 'XD'
__mtime__ = 18-7-27
__IDE__ = PyCharm
Fix the Problem, Not the Blame.
'''
import hashlib
import requests
import json
import pprint
def get_token_text(student_num):
    '''
    获取动态的token
    :param student_num: 学号
    :return: str
    '''
    # mod5加密, 传入头
    p_text = hashlib.md5(student_num.encode('utf-8')).hexdigest()
    header = {'Content-Type': 'application/json; charset=utf-8',
              'User-Agent': 'okhttp/3.3.1'
              }
    data = {
        "u": student_num,
        "p": p_text
    }
    url = 'http://42.244.42.160/university-facade/Murp/Login'
    # 访问
    response = requests.post(url, data=json.dumps(data), headers=header)
    token_text = json.loads(response.text)['data']['token']
    return token_text


def get_all_result(token):
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
    return response.text


token = get_token_text('1809401020')
result = json.loads(get_all_result(token))
grades = result['data']
pprint.pprint(grades)
