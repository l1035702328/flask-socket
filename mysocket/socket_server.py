# -*- coding: utf-8 -*-
# @Time    : 2022/8/31 11:35
# @Author  : LZZ
# @FileName: socket_server.py
# @Software: PyCharm


from socketserver import BaseRequestHandler, ThreadingTCPServer, TCPServer, ThreadingMixIn
from typing import Tuple

from flask_script import Command
import redis
import re
import logging


class MyServer(BaseRequestHandler):

    """
    必须继承socketserver.BaseRequestHandler类
    """
    def setup(self):
        print("从连接池抽取连接")
        self.redis_conn = self.server.redis_conn
        self.num = 0

    def handle(self):
        """
        必须实现这个方法！
        :return:
        """
        conn = self.request         # request里封装了所有请求的数据
        conn.sendall('欢迎访问socketserver服务器!\0'.encode())
        data = conn.recv(1024).decode()
        print(data)
        name = re.search('(?<=name:)\w+', data).group()
        flag = {'power_flag': '0', 'upgrade_flag': '0', 'filename': '0'}
        self.redis_conn.hset("{}_flag".format(name), mapping=flag)
        self.redis_conn.sadd('register_id', name)
        while True:
            print("创建的连接个数{}".format(self.redis_conn.connection_pool._created_connections))
            print("连接池连接列表{}".format(self.redis_conn.connection_pool._available_connections))
            self.num += 1
            print("线程内部循环累加器{}".format(self.num))
            print("进入循环")
            data = conn.recv(1024).decode()
            if not data:
                print("断开与%s的连接！" % (self.client_address,))
                break
            print("来自%s的客户端向你发来信息：%s" % (self.client_address, data))
            conn.sendall(('已收到你的消息<%s>\0' % data).encode())
            try:
                name = re.search('(?<=name:)\w+', data).group()

                result_num = self.redis_conn.rpush(name, data)
                print("插入成功")
                result = self.redis_conn.hgetall(name + '_flag')
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
            except AttributeError as e:
                print("name未匹配到正常参数,结束")
                break
            print("跳出")


class MyTCPServer(TCPServer):
    def __init__(self, server_address: Tuple[str, int], RequestHandlerClass, bind_and_activate=True, redis_conn=None):
        super(MyTCPServer, self).__init__(server_address, RequestHandlerClass, bind_and_activate)
        self.redis_conn = redis_conn


class MyThreadingTCPServer(ThreadingMixIn, MyTCPServer): pass


class SocketRun(Command):
    def run(self):
        # 创建logger实例
        logging.basicConfig(handlers=[logging.FileHandler(filename="./hxya.log",
                            encoding='utf-8', mode='a+')], level=logging.DEBUG,
                            format='%(asctime)s %(message)s', datefmt='%Y/%m/%d %I:%M:%S')
        logging.debug('debug 信息')
        logging.info("hello")
        redis_pool = redis.ConnectionPool(host='119.91.55.183', port=6379, password='1156989490', db=1,
                                          decode_responses=True)
        redis_conn = redis.Redis(connection_pool=redis_pool)
        print("初始化线程池完毕")
        # 创建一个多线程TCP服务器
        server = MyThreadingTCPServer(('127.0.0.1', 6000), MyServer, redis_conn=redis_conn)
        with server:
            print("启动socketserver服务器！")
            # 启动服务器，服务器将一直保持运行状态
            server.serve_forever()
