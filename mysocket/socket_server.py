# -*- coding: utf-8 -*-
# @Time    : 2022/8/31 11:35
# @Author  : LZZ
# @FileName: socket_server.py
# @Software: PyCharm


from socketserver import BaseRequestHandler, ThreadingTCPServer
from flask_script import Command
import redis
import re
import logging


class MyServer(BaseRequestHandler):

    """
    必须继承socketserver.BaseRequestHandler类
    """
    def setup(self):
        print("初始化连接池")
        self.redis_pool = redis.ConnectionPool(host='119.91.55.183', port=6379, password='1156989490', db=1, decode_responses=True)

    def handle(self):
        """
        必须实现这个方法！
        :return:
        """
        conn = self.request         # request里封装了所有请求的数据
        conn.sendall('欢迎访问socketserver服务器！'.encode())
        data = conn.recv(1024).decode()
        name = re.search('(?<=name:)\w+', data).group()
        flag = {'power_flag': '0', 'upgrade_flag': '0', 'filename': '0'}
        redis_conn = redis.Redis(connection_pool=self.redis_pool)
        redis_conn.hset("{}_flag".format(name), mapping=flag)
        while True:
            data = conn.recv(1024).decode()
            if data == "exit":
                print("断开与%s的连接！" % (self.client_address,))
                break
            print("来自%s的客户端向你发来信息：%s" % (self.client_address, data))
            conn.sendall(('已收到你的消息<%s>' % data).encode())
            name = re.search('(?<=name:)\w+', data).group()

            redis_conn = redis.Redis(connection_pool=self.redis_pool)
            result_num = redis_conn.rpush(name, data)
            logging.info("插入成功")
            result = redis_conn.hgetall(name + '_flag')
            logging.info("获取flag成功")
            print(result)
            if result['power_flag'] == '1':
                print("执行关闭电源指令")
            if result['upgrade_flag'] == '1':
                msg = "msg:upgrade;flag:1"
                conn.sendall(('发送确认升级指令,下位机接受状态:{}'.format(msg)).encode())
                data = conn.recv(1024).decode()
                if data == 'ok':
                    print("去调文件")
                # 升级完成应重置状态
            print("跳出")



class SocketRun(Command):
    def run(self):
        # 创建logger实例
        logging.basicConfig(handlers=[logging.FileHandler(filename="./hxya.log",
                            encoding='utf-8', mode='a+')], level=logging.DEBUG,
                            format='%(asctime)s %(message)s', datefmt='%Y/%m/%d %I:%M:%S')
        logging.debug('debug 信息')
        logging.info("hello")
        # 创建一个多线程TCP服务器
        server = ThreadingTCPServer(('127.0.0.1', 6000), MyServer)
        with server:
            print("启动socketserver服务器！")
            # 启动服务器，服务器将一直保持运行状态
            server.serve_forever()
