# -*- coding: utf-8 -*-
# @Time    : 2022/8/18 16:02
# @Author  : LZZ
# @FileName: __init__.py.py
# @Software: PyCharm

import os

import pymysql
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from config import config
from myflask.user import user

app = Flask(__name__)
pymysql.install_as_MySQLdb()
db = SQLAlchemy()
# app.config['SECRET_KEY'] = 'secret!'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@119.91.55.183/flask_study'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

def create_app(config_name):
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    db.init_app(app)
    # 注册路由
    app.register_blueprint(user, url_prefix='/')
    return app
