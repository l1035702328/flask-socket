# -*- coding: utf-8 -*-
# @Time    : 2022/8/18 15:34
# @Author  : LZZ
# @FileName: models.py
# @Software: PyCharm


# 用户的模型类
from datetime import datetime
from myflask import db, bcrypt


class User(db.Model):
    __tablename__='t_user'
    id=db.Column(db.BIGINT,primary_key=True,autoincrement=True)
    username=db.Column(db.String(64),doc='用户名')
    password=db.Column(db.String(64),doc='密码')
    email=db.Column(db.String(100),doc='邮箱')
    phone=db.Column(db.String(11),doc='手机号')
    login_time=db.Column(db.DateTime,default=datetime.now(),doc='登录时间')
    create_time=db.Column(db.DateTime,default=datetime.now(),doc='用户注册时间')
    update_time=db.Column(db.DateTime,default=datetime.now(),onupdate=datetime.now(),doc='用户修改时间')
    status=db.Column(db.Integer,doc='用户状态')
    role_id = db.Column(db.Integer, db.ForeignKey('t_roles.id'))
    role = db.relationship('Role', backref='user_of_role')

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password)
    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

    def __repr__(self):
        return '<User {} pwd {}>'.format(self.username, self.password)

class Role(db.Model):
     __tablename__ = 't_roles'
     id = db.Column(db.Integer, primary_key=True)
     name = db.Column(db.String(64), unique=True)


     def __repr__(self):
        return '<Role %r>' % self.name

