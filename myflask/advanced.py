# -*- coding: utf-8 -*-
# @Time    : 2022/8/25 11:08
# @Author  : LZZ
# @FileName: advanced.py
# @Software: PyCharm
from flask_apscheduler import scheduler

from myflask import app




def job2():
    # 定时采集redis的数据上传至mysql
    print("执行定时采集作业")
    redis_client = app.config.redis
    # 获取集合元素
    register_id = redis_client.smembers("register_id")
    print(register_id)
    for my_id in register_id:
        with redis_client.pipeline() as pipe:
            datas = pipe.lrange(my_id, 0, -2)
            print(datas)
            print("执行写入数据库操作 如果失败则不执行删除操作")
            result = pipe.ltrim(my_id, -1, -1)
            print(result)
            if result:
                print("删除成功")
            else:
                print("删除失败")

