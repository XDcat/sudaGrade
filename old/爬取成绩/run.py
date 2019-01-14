from api import departments_number
from  api.GPAcalculator import *
from api.tokenget import *
from pprint import pprint


def get_body_info(xh):  #获取个人的学号，姓名，所有成绩
    headers = {
        "Content-Type": "application/json;charset=utf-8",
        "User-Agent": "Mozilla/5.0 (Linux; U; Android 8.0.0; zh-cn; MI 6 Build/OPR1.170623.027) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/61.0.3163.128 Mobile Safari/537.36 XiaoMi/MiuiBrowser/9.7.2 "
        }
    info = GetPersonInfo(xh) #获取含有名字，学号，token的字典
    if info == 0:
        return 0
    token = info['token']
    curl = 'http://42.244.42.160//university-facade/MyUniversity/MyGrades?token={0}'.format(token)
    mark = json.loads(requests.get(curl,headers = headers).text)['data']   #这里和get_json耦合，后期简化一下
    if mark == None:
        mark = '没做教学评测'
    person_in = {}
    person_in['xh'] = info['xh']
    person_in['name'] = info['name']
    # pprint.pprint(total)
    total =dict()
    total['person'] = person_in
    total['mark'] = mark
    return total

def print_gpa_on_screen():
    no_start = eval(input('请输入开始学号：'))
    no_end = eval(input('请输入结束学号：'))
    for i in range(no_start,no_end+1):
        if get_body_info(i) != 0:
            try:
                xh = get_body_info(i)['person']['xh']
                name = get_body_info(i)['person']['name']
                mark = get_body_info(i)['mark']
                if mark == '没做教学评测':
                    print(xh,name,mark)
                    continue
                gpa = C_GPA(mark)
                print(xh,name,gpa)
            except Exception:
                print(get_body_info(i))

def output_allmarks_into_txt(path):
    w = open('C:\\Users\\S\Desktop\\aaaaaa\\marks\\all_2016.txt','w')
    with open(path,'r',encoding='utf-8') as f:
        for i in f.readlines():
            output_one =''
            res = json.loads(i)
            name = res['name']
            no = res['num']
            department = departments_number.department[no[2:7]]
            output_one += department + ','+ no + ',' + name + '\n'
            # pprint.pprint(res)
            if res['data']['data'] == None:
                output_one += '\n' * 20
                continue
            for j in res['data']['data']:
                for k in j['items']:
                    if 'cj' in k and k['cj'].isdigit():
                        cj = k['cj']
                        kcmc = k['kcmc']
                        kcdm = k['kcdm']
                        if 'kcxz' in k:
                            kcxz = k['kcxz']
                        else:
                            kcxz = ''
                        xf = k['xf']
                        output_one += ' '+','+' '+','+' '+','+ kcmc + ',' + kcdm + ',' + kcxz + ',' + xf + ',' + cj + '\n'
            output_one += '总绩点：'+',' + str(C_GPA(res['data']['data'])) + '\n' *3
            w.write(output_one)
            print(no,name,'已完成爬取')
        w.close()

def output_gpa(path):
    w = open('C:\\Users\\S\Desktop\\aaaaaa\\marks\\all_gpa_2016','w')
    with open(path,'r') as f:
        for i in f.readlines():
            output_one = ''
            res = json.loads(i)
            name = res['name']
            no = res['num']
            department = departments_number.department[no[2:7]]
            if res['data']['data'] == None:
                continue
            else:
                mark = res['data']['data']
                gpa = C_GPA(mark)
                output_one += department +',' + no + ',' + name +',' + '{0:.3f}'.format(gpa) + '\n'
                w.write(output_one)
                print(output_one)
if __name__ == '__main__':
    # output_allmarks_into_txt('C:\\Users\\S\\Desktop\\aaaaaa\\json\\2016_json.txt')
    # output_gpa('C:\\Users\\S\\Desktop\\aaaaaa\\json\\2016_json.txt')
    pprint(get_body_info(1709404067))