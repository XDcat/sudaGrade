from api.tokenget import *
from api.departments_number import department
import json
import requests
from pprint import pprint
import re
import time

def get_json(path):
    headers = {
        "Content-Type": "application/json;charset=utf-8",
        "User-Agent": "Mozilla/5.0 (Linux; U; Android 8.0.0; zh-cn; MI 6 Build/OPR1.170623.027) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/61.0.3163.128 Mobile Safari/537.36 XiaoMi/MiuiBrowser/9.7.2 "
        }
    w = open( 'C:\\Users\\S\\Desktop\\aaaaaa\\json\\'+re.search('\d+',path).group(0) + '_json.txt','w')
    print('aaaa')
    with open(path,'r') as f:
        lines = f.readlines()
        length = len(lines)
        k = 0
        for i in lines:
            k += 1
            if k%100 == 0:
                time.sleep(1)
            line = i.split()
            department = line[0]
            number = line[1]
            name = line[2]
            token = line[3]
            curl = 'http://42.244.42.160//university-facade/MyUniversity/MyGrades?token={0}'.format(token)
            print(token)
            try:
                data = json.loads(requests.get(url=curl,headers=headers,timeout = 3).text)
            except Exception as e:
                print(number, e)
                time.sleep(3)
                data = json.loads(requests.get(url=curl,headers=headers,timeout = 3).text)
            if data['message'] == "您的账号在其他地方登录，请注意账号安全":
                token = GetPersonInfo(number)['token']
                curl = 'http://42.244.42.160//university-facade/MyUniversity/MyGrades?token={0}'.format(token)
                data = json.loads(requests.get(url=curl, headers=headers,timeout = 3).text)
            _data = {}
            _data['num'] = number
            _data['name'] = name
            _data['data'] = data
            output = json.dumps(_data) + '\n'
            w.write(output)
            print(number + ' ' + name + ' 已完成({0}/{1})'.format(k,length))

if __name__ == '__main__':
    get_json('C:\\Users\\S\\Desktop\\aaaaaa\\numbers\\2016_numbers.txt')

