# -*- coding:utf-8 -*-
'''
__author__ = 'XD'
__mtime__ = 2019/1/14
__project__ = 教学评估解析
Fix the Problem, Not the Blame.
'''
import json
from pprint import pprint


class WeiXinStu():
    def __init__(self, data):
        self.GPA = 0  # 总绩点
        self.termGPA = []  # 学期绩点
        self.gradeOfRank = []  # 带有等级的成绩
        self.Xf = 0  # 总学分
        self.termXf = []  # 学期学分
        self.__initialize(data)
        self.gradeRank = self.lowGrade(data)
    def __str__(self):
        doc = []
        doc.append('学习报表')
        doc.append('GPA：{}'.format(self.GPA))
        doc.append('总学分：{}'.format(self.Xf))
        [doc.append('{}GPA：{}'.format(i, j)) for i, j in self.termGPA]
        [doc.append('{}学分：{}'.format(i, j)) for i, j in self.termXf]
        doc.append('带等级的成绩：')
        [doc.append('{}：{}'.format(i, j)) for i, j in self.gradeOfRank]
        return '\n'.join(doc)
    @staticmethod
    def g(point):
        '''
        获取分数对于的G点
        :param point: 分数
        :return: G点
        '''
        point = int(point)
        gpadb = {100: 4.0, 79: 3.2,
                 99: 4.0, 78: 3.1,
                 98: 4.0, 77: 3.0,
                 97: 4.0, 76: 2.9,
                 96: 4.0, 75: 2.8,
                 95: 4.0, 74: 2.7,
                 94: 3.9, 73: 2.6,
                 93: 3.9, 72: 2.5,
                 92: 3.9, 71: 2.4,
                 91: 3.8, 70: 2.3,
                 90: 3.8, 69: 2.2,
                 89: 3.8, 68: 2.1,
                 88: 3.7, 67: 2.0,
                 87: 3.7, 66: 1.8,
                 86: 3.6, 65: 1.7,
                 85: 3.6, 64: 1.6,
                 84: 3.5, 63: 1.4,
                 83: 3.5, 62: 1.3,
                 82: 3.4, 61: 1.1,
                 81: 3.3, 60: 1.0,
                 80: 3.3}
        if point < 60:
            return 0
        else:
            return gpadb[point]

    @staticmethod
    def getXn(t):
        '''
        根据数字返回学年
        :param y: 第几个学期, 从0开始
        :return: 大几
        '''
        num = {
            1: '一',
            2: '二',
            3: '三',
            4: '四',
            5: '五',
            6: '六',
            7: '七',
            8: '八'
        }
        xn = num[int(t / 2) + 1]  # 学年
        if t % 2 == 0:
            xq = '上'
        else:
            xq = '下'
        return '大{}（{}）'.format(xn, xq)
    def lowGrade(self, data):
        data = json.loads(data, encoding='utf-8')['data']
        termList = sorted(data['termList'])  # 排序确定学年
        gradeRank = {}
        for i in termList:
            for j in data[i]:
                name = j['name']
                score = j['score']
                if score.isdigit():
                    G = self.g(score)
                    gradeRank.setdefault(G, [])
                    gradeRank[G].append((name, score))
        return gradeRank
    def __initialize(self, data):
        # json解析
        data = json.loads(data, encoding='utf-8')['data']
        termList = sorted(data['termList'])  # 排序确定学年
        # 计算学分和GPA
        sumAllXf = 0  # 所有的学分
        sumAllXfForG = 0  # 计算学分所用的学分
        sumAllG = 0  # 所有的G点
        for i in termList:
            # 到某一个确定的学期
            term = data[i]
            sumXf = 0  # 总共的学分
            sumXfForG = 0  # 计算学分用的
            sumG = 0  # 总共的G点
            for j in term:
                # 到某一个确定的成绩
                score = j['score']
                if not score.isdigit():
                    sumXf += xf
                    self.gradeOfRank.append((j['name'], score))
                    continue
                G = self.g(score)
                xf = float(j['xf'])
                # 加合
                sumG += G * xf
                sumXf += xf
                sumXfForG += xf
            # 总绩点的计算
            sumAllG += sumG
            sumAllXf += sumXf
            sumAllXfForG += sumXfForG
            # 计算当前学期的
            termGPA = '{:.3}'.format(sumG / sumXfForG)
            self.termGPA.append((self.getXn(termList.index(i)), termGPA))
            self.termXf.append((self.getXn(termList.index(i)), sumAllXf))
        GPA = '{:.3}'.format(sumAllG / sumAllXfForG)
        self.GPA = GPA
        self.Xf = sumAllXf
        # print("{},GPA={}".format('总计', GPA))
        # pprint(data)


if __name__ == '__main__':
    data = '{"errorcode":0,"success":true,"msg":"","data":{"2018-2019学年第一学期":[{"name":"中国近现代史纲要","score":"A","kcxz":"公共基础课程","xf":"2","kcdm":"00021015"},{"name":"有机化学实验（二）","score":"87","kcxz":"大类基础课程","xf":"2","kcdm":"CHET1002"},{"name":"有机化学（二）（下）","score":"84","kcxz":"大类基础课程","xf":"2","kcdm":"CHET2004"},{"name":"物理化学（二）（上）","score":"94","kcxz":"大类基础课程","xf":"2","kcdm":"CHET2041"},{"name":"识谱与歌唱","score":"B","kcxz":"公共选修课程","xf":"2","kcdm":"00211103"},{"name":"生活中的高分子材料","score":"94","kcxz":"通识选修课程","xf":"2","kcdm":"TX095002"},{"name":"普通物理实验","score":"87","kcxz":"公共基础课程","xf":"1","kcdm":"00081010"},{"name":"公共体育（三）","score":"B","kcxz":"公共基础课程","xf":"1","kcdm":"00061007"},{"name":"工程数学","score":"92","kcxz":"专业必修课程","xf":"4","kcdm":"CHET2021"},{"name":"工程力学","score":"90","kcxz":"专业必修课程","xf":"2","kcdm":"MSEN2016"},{"name":"电工电子学","score":"90","kcxz":"专业必修课程","xf":"2","kcdm":"MSEN2013"},{"name":"大学英语（三）","score":"78","kcxz":"公共基础课程","xf":"2","kcdm":"00041003"}],"2017-2018学年第二学期":[{"name":"有机化学（二）（上）","score":"88","kcxz":"大类基础课程","xf":"3","kcdm":"CHET2039"},{"name":"无机及分析化学实验","score":"91","kcxz":"大类基础课程","xf":"1.5","kcdm":"CHET2024"},{"name":"普通物理（二）（上）","score":"90","kcxz":"公共基础课程","xf":"4","kcdm":"00081002"},{"name":"机械设计基础","score":"82","kcxz":"大类基础课程","xf":"3","kcdm":"CHET1001"},{"name":"公共体育（二）","score":"B","kcxz":"公共基础课程","xf":"1","kcdm":"00061002"},{"name":"高等数学（一）下","score":"90","kcxz":"公共基础课程","xf":"5","kcdm":"00071013"},{"name":"分析化学（二）","score":"86","kcxz":"大类基础课程","xf":"2","kcdm":"CHET2023"},{"name":"大学英语（二）","score":"81","kcxz":"公共基础课程","xf":"2","kcdm":"00041028"},{"name":"VB程序设计","score":"95","kcxz":"公共基础课程","xf":"4","kcdm":"00271002"}],"2017-2018学年第一学期":[{"name":"中国地方文化英语教学","score":"85","kcxz":"通识选修课程","xf":"2","kcdm":"TX041004"},{"name":"职业生涯规划指导（上）","score":"A","kcxz":"公共基础课程","xf":"0.5","kcdm":"00361005"},{"name":"形势与政策","score":"A","kcxz":"公共基础课程","xf":"2","kcdm":"00021034"},{"name":"无机化学（二）","score":"75","kcxz":"大类基础课程","xf":"2","kcdm":"CHET2022"},{"name":"文献检索","score":"91","kcxz":"跨专业选修课程","xf":"2","kcdm":"CHEM1058"},{"name":"军事技能","score":"B","kcxz":"公共基础课程","xf":"1","kcdm":"00351003"},{"name":"计算模拟——化学家的新工具","score":"97","kcxz":"新生研讨课程","xf":"2","kcdm":"YT091009"},{"name":"计算机信息技术Ⅰ","score":"84","kcxz":"公共基础课程","xf":"3","kcdm":"00270007"},{"name":"公共体育（一）","score":"B","kcxz":"公共基础课程","xf":"1","kcdm":"00061001"},{"name":"高等数学（一）上","score":"87","kcxz":"公共基础课程","xf":"5","kcdm":"00071012"},{"name":"大学英语（一）","score":"80","kcxz":"公共基础课程","xf":"4","kcdm":"00041001"}],"termList":["2018-2019学年第一学期","2017-2018学年第二学期","2017-2018学年第一学期"]}}'
    # data = '{"errorcode":0,"success":true,"msg":"","data":{"2018-2019学年第一学期":[{"name":"数据结构","score":"97","kcxz":"大类基础课程","xf":"4","kcdm":"SOEN2029"},{"name":"普通物理实验","score":"88","kcxz":"公共基础课程","xf":"1","kcdm":"00081010"},{"name":"马克思主义基本原理","score":"A","kcxz":"公共基础课程","xf":"3","kcdm":"00021014"},{"name":"离散数学","score":"95","kcxz":"大类基础课程","xf":"4","kcdm":"COMS2022"},{"name":"军事理论","score":"B","kcxz":"公共基础课程","xf":"2","kcdm":"00351001"},{"name":"黄金珠宝防伪与鉴赏","score":"83","kcxz":"通识选修课程","xf":"2","kcdm":"TX095004"},{"name":"公共体育（三）","score":"B","kcxz":"公共基础课程","xf":"1","kcdm":"00061007"},{"name":"公共关系学","score":"A","kcxz":"公共选修课程","xf":"2","kcdm":"00021105"},{"name":"大学英语（三）","score":"75","kcxz":"公共基础课程","xf":"2","kcdm":"00041003"}],"2017-2018学年第二学期":[{"name":"有机化学（二）（上）","score":"88","kcxz":"其他课程","xf":"3","kcdm":"CHET2039"},{"name":"无机及分析化学实验","score":"86","kcxz":"其他课程","xf":"1.5","kcdm":"CHET2024"},{"name":"普通物理（二）（上）","score":"86","kcxz":"公共基础课程","xf":"4","kcdm":"00081002"},{"name":"机械设计基础","score":"83","kcxz":"其他课程","xf":"3","kcdm":"CHET1001"},{"name":"公共体育（二）","score":"B","kcxz":"公共基础课程","xf":"1","kcdm":"00061002"},{"name":"高等数学（一）下","score":"88","kcxz":"公共基础课程","xf":"5","kcdm":"00071013"},{"name":"分析化学（二）","score":"81","kcxz":"其他课程","xf":"2","kcdm":"CHET2023"},{"name":"大学英语（二）","score":"82","kcxz":"公共基础课程","xf":"2","kcdm":"00041028"},{"name":"VB程序设计","score":"95","kcxz":"其他课程","xf":"4","kcdm":"00271002"}],"termList":["2018-2019学年第一学期"]}}'
    xx = WeiXinStu(data)
    print(xx)
    pprint(xx.gradeRank)