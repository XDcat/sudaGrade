import requests
from lxml import etree
from pprint import pprint


def test_proxy(token):
    """获取个人信息列表"""
    header = {'Content-Type': 'application/json; charset=utf-8',
              'User-Agent': 'okhttp/3.3.1'
              }
    # 获取待评测列表
    url = 'http://42.244.42.160/university-facade/MyUniversity/StudyState?token={}&suno=null'.format(
        token)
    try:
        res = requests.get(url, headers=header, timeout=5)
        return res
    except:
        return None


header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
}
res = requests.get('https://www.xicidaili.com/nn/', headers=header)
html = etree.HTML(res.text)
ip = html.xpath("//table[@id='ip_list']/tr[position() > 1]/td[2]/text()")
port = html.xpath("//table[@id='ip_list']/tr[position() > 1]/td[3]/text()")
type = html.xpath("//table[@id='ip_list']/tr[position() > 1]/td[6]/text()")
if len(ip) == len(port) == len(type) and len(ip) > 0:
    res = zip(ip, port, type)
    proxies = []
    for i in res:
        proxy = {i[2].lower(): 'http://{}:{}'.format(i[0], i[1])}
        test = test_proxy('ab664a777558452794a38f35810d5090')
        if test.text[
           :100] == '{"data":[{"v":"龚志强","k":"姓名"},{"v":"1809404002","k":"学号"},{"v":"男","k":"性别"},{"v":"材料与化学化工学部","k":"学':
            proxies.append(proxy)
    pprint(proxies)
else:
    print(res.text)
