# -*- coding:utf-8 -*-
"""
__author__ = 'XD'
__mtime__ = 2019/1/25
__project__ = 教学评估解析
Fix the Problem, Not the Blame.
"""
import json
import sqlite3


def dict_factory(cursor, row):
    """Cursor的工厂方法：返回字典"""
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def select_all(table):
    """获取表中所有数据"""
    con = sqlite3.connect('db/sudaStu.db')
    con.row_factory = dict_factory  # 指定工厂方法
    res = con.execute('SELECT * FROM {}'.format(table)).fetchall()
    con.close()
    return res


def has_num(num):
    """数据库中是否存在num学号"""
    con = sqlite3.connect('db/sudaStu.db')
    con.row_factory = dict_factory  # 指定工厂方法
    res = con.execute('SELECT * FROM stu WHERE stuNum = ?', (num,)).fetchone()
    con.close()
    return res


def insert_stu(num, isLogable, token, name, score, GPA, info):
    """
    保存数据
    :param num: 学号
    :param isLogable: 是否可登陆
    :param token: ~
    :param name: 姓名
    :param grade: 成绩
    :return: None
    """
    con = sqlite3.connect('db/sudaStu.db')
    con.execute('INSERT INTO stu (stuNum, isLogable, token, name, score, GPA, info) VALUES (?, ?, ?, ?, ?, ?, ?)',
                (num, isLogable, token, name, json.dumps(score), str(GPA), json.dumps(info)))
    con.commit()
    con.close()


def insert_major(num, grade, academy, major):
    """
    保存major信息
    :param num: 编号
    :param grade: 年级
    :param academy: 学院
    :param major: 专业
    :return:
    """
    con = sqlite3.connect('db/sudaStu.db')
    con.execute('INSERT INTO major (num, grade, academy, major) VALUES (?, ?, ?, ?)',
                (num, grade, academy, major))
    con.commit()
    con.close()
