# -*- coding: utf-8 -*-
# @Time    : 2022/8/25 11:08
# @Author  : LZZ
# @FileName: advanced.py
# @Software: PyCharm
from flask_apscheduler import scheduler




def job2(var_one=3, var_two=7):
    """Demo job function.
    :param var_two:
    :param var_two:
    """
    print(str(var_one) + " " + str(var_two))
