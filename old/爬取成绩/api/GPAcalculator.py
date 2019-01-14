def g(point):
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


def C_GPA(mark):
    jiaquan = 0
    xuefen_total = 0
    for i in mark:  # 遍历学年学期
        for j in i['items']:  # 遍历学年学期里的存成绩的列表
            if 'cj' not in j:
                continue
            cj = j['cj']
            if cj.isdigit():
                cj = eval(cj)
            else:
                continue
            xf = eval(j['xf'])
            gpa = g(cj)
            if gpa == 0:
                continue
            jiaquan += xf * gpa
            xuefen_total += xf
    if xuefen_total == 0:
        return 0
    return jiaquan / xuefen_total
