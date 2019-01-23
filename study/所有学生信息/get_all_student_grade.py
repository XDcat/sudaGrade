# ~/annaconda3/bin/python3.6
# -*- coding:utf-8 -*-
'''
__author__ = 'XD'
__mtime__ = 18-7-29
__IDE__ = PyCharm
Fix the Problem, Not the Blame.
'''
import hashlib
import requests
import json
import pprint
import re
import random

def get_token_text(student_num):
    '''
    获取动态的token
    :param student_num: 学号
    :return: str
    '''
    # mod5加密, 传入头
    proxy = {'http': 'http://219.141.153.3'}
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
    response = requests.post(url, data=json.dumps(data), headers=header, proxies=proxy, timeout=6)
    token_text = json.loads(response.text)['data']['token']
    return token_text


def get_all_result(token):
    '''
    获取成绩信息
    :param token: token参数
    :return:
    '''
    ip_pool = [{'http': 'http://219.141.153.3'},
               {'http': 'http://219.141.153.35'},
               {'http': 'http://219.141.153.4'},
               {'http': 'http://219.141.153.38'},
               {'http': 'http://219.141.153.40'}]
    proxy = random.choice(ip_pool)
    header = {'Content-Type': 'application/json; charset=utf-8',
              'User-Agent': 'okhttp/3.3.1'
              }
    url = 'http://42.244.42.160//university-facade/MyUniversity/MyGrades?token={}'.format(token)
    while True:
        try:
            response = requests.get(url, headers=header, proxies=proxy, timeout=5)
            break
        except Exception as e:
            print('连接错误, 再次尝试！', e)
    return json.loads(response.text)


def main():
    with open('./data/all_student_grade.txt') as f:
        num_l = []
        for i in f.readlines():
            num_l.append(json.loads(i)['num'])


    with open('./data/all_students.txt') as f:
        for i in f.readlines():
            # 获取学号, 姓名, token
            num = i.split()[0]
            name = i.split()[1]
            token = re.compile("'token': '(.{32})'").search(i).group(1)
            if num not in num_l:  # 已经获取的数据排除
                # 保存数据地址
                with open('./data/all_student_grade.txt', 'a') as f_1:
                    # 数据格式
                    student = {'num': num,
                               'name': name,
                               }
                    grade = get_all_result(token)
                    if grade['state'] != 200:
                        # 如果不成功则再次取出token
                        token = get_token_text(num)
                        # 再次获取数据, 肯定能够成功
                        grade = get_all_result(token)
                        print('token发生改变， 重新获取：' + token, grade)
                    # 保存数据
                    student['data'] = grade
                    f_1.write(json.dumps(student) + '\n')
                    print(num, '获取数据成功')
            else:
                print(num, '已经获取')

if __name__ == '__main__':
    main()
