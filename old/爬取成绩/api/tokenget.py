import json

import requests

from api import md5p


def GetPersonInfo(xh):
    k = 0
    try:
        headers = {
            "Content-Type": "application/json;charset=utf-8",
            "Content-Length": "148",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "User-Agent": "Mozilla/5.0 (Linux; U; Android 8.0.0; zh-cn; MI 6 Build/OPR1.170623.027) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/61.0.3163.128 Mobile Safari/537.36 XiaoMi/MiuiBrowser/9.7.2 ",
            "Host": "42.244.42.160"
    }

        p = md5p.GetUltraP(xh)

        data = {
        "u":"{0}".format(xh),
        "uuid":"008796763732113",
        "ver":109,
        "type":"110",
        "tec":"android:4.4.4",
        "p":"{0}".format(p)
    }
        post_url = 'http://42.244.42.160/university-facade/Murp/Login'
        res = requests.post(url=post_url,data = json.dumps(data) ,headers = headers)
        final_dict = json.loads(res.text)
        if final_dict['message'] == '用户名或密码不正确！':
            # print('用户{0}改过密码，或该用户不存在'.format(xh))
            return 0
        person_info = {}
        person_info['xh'] = str(xh)
        person_info['name'] = final_dict['data']['name']
        person_info['token'] = final_dict['data']['token']
        return person_info
    except Exception as e:
        print("该学号无法爬取token,错误类型：",e)
        # print('正在重试……')
        if k > 3:
            print('{0}重试超过3次，停止重试，记录错误到日志'.format(xh))
            with open('errorlog.txt','w') as f:
                f.write('{0}  错误:{1}\n'.format(xh,e))
            return
        # GetPersonInfo(xh)
        k += 1

if __name__ == '__main__':
    a = GetPersonInfo(1709404067)
    print(a)
