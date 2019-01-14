from api import departments_number
from api.tokenget import *
import time


def build_number(grade, department, no):
    number = int(str(grade)[2:] + department + str(no))
    return number

def getgrade(grade):
    w = open('C:\\Users\\S\Desktop\\aaaaaa\\numbers\\{0}_numbers.txt'.format(grade),'w')
    w1 = open('{0}_fault_numbers.txt'.format(grade),'w')
    for i in departments_number.department:
        judge_dict = []
        k = 0
        for j in range(build_number(grade, i, '001'), build_number(grade, i, 300) + 1):
            try:
                flag = GetPersonInfo(j)
                while flag == None:
                    time.sleep(5)
                    flag = GetPersonInfo(j)
                if flag != 0:
                    xh = flag['xh']
                    name = flag['name']
                    token = flag['token']
                    output = str(departments_number.department[i]) + ' ' + str(xh) + ' ' + str(name) + ' ' + str(token) + '\n'
                    w.write(output)
                    print(output)
                else:
                    w1.write(str(j) + '\n')
                    k += 1
                    if k%20 == 0:
                        judge_dict = []
                    judge_dict.append(j)
                    if j-1 in judge_dict and j-2 in judge_dict and j-3 in judge_dict:
                        break
            except Exception as e:
                print(e,j)
        time.sleep(3)
    w.close()
    w1.close()


if __name__ == '__main__':
    getgrade(2016)
