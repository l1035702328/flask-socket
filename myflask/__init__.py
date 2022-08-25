# -*- coding: utf-8 -*-
# @Time    : 2022/8/18 16:02
# @Author  : LZZ
# @FileName: __init__.py.py
# @Software: PyCharm


import pymysql
from apscheduler.schedulers.blocking import BlockingScheduler
from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_apscheduler import APScheduler
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from config import config
from flask_bcrypt import Bcrypt
from myflask import advanced

pymysql.install_as_MySQLdb()
db = SQLAlchemy()
bcrypt = Bcrypt()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    # jwt鉴权
    jwt = JWTManager()
    jwt.init_app(app)
    # 数据库db
    db.init_app(app)
    # 初始化字段
    init_user(app)
    # 使用admin管理
    register_extensions(app)
    # 注册路由
    from myflask.user import user
    app.register_blueprint(user, url_prefix='/')

    # 定时任务
    scheduler = APScheduler()
    scheduler.init_app(app)
    scheduler.add_job('job2', func=advanced.job2, trigger='interval', seconds=3, args=["desire"], replace_existing=True)
    scheduler.start()

    return app

# admin管理
def register_extensions(app):
    from myflask.models import User, Role
    admin = Admin(app, name='microblog', template_mode='bootstrap3')
    admin.add_view(ModelView(User, db.session))
    admin.add_view(ModelView(Role, db.session))

# 初始用户
def init_user(app):
    from myflask.models import User, Role
    with app.app_context():
        result = User.query.filter(User.id < 5).delete()
        result = Role.query.filter(Role.id < 5).delete()
        role_admin = Role(id=1, name='admin')
        role_guest = Role(id=2, name='guest')
        db.session.add(role_admin)
        db.session.add(role_guest)
        user_admin = User(id=1, username='admin', email='1156989490@qq.com', phone='13466987412', status='1', role_id=1)
        user_admin.set_password('admin')
        print(user_admin)
        db.session.add(user_admin)
        db.session.commit()


