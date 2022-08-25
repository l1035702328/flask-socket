# -*- coding: utf-8 -*-
# @Time    : 2022/8/12 11:26
# @Author  : LZZ
# @FileName: user.py
# @Software: PyCharm

from flask import Blueprint, jsonify, request
from flask.views import MethodView
from flask_jwt_extended import create_access_token
from myflask.models import User
from utils.mixin import LoginRequiredMixin

user = Blueprint('user_view', __name__)

class LoginView(MethodView):
    def get(self):
        return "render_template('user.html')"

    def post(self):
        username = request.form.get('username')
        password = request.form.get('password')
        if all([username, password]) is None:
            return "数据为空"
        req_user = User(username=username)
        req_user.set_password(password)
        user= User.query.filter(User.username==username).first()
        if user:
            print('查询的user{}'.format(user.password))
            result = user.check_password(password)
            if result:
                access_token = create_access_token(identity=username)
                print("登录成功")
                return jsonify(access_token=access_token)
            else:
                print("密码错误")
        else:
            return "未找到该用户"


class RegisterView(MethodView):
    def post(self,request):
        username = request.POST.get('username')
        password = request.POST.get('pwd')
        email = request.POST.get('email')
        allow = request.POST.get('allow')


class IndexView(LoginRequiredMixin, MethodView):
    def get(self):
        return "hello this is index"


user.add_url_rule('/', endpoint='index', view_func=IndexView.as_view('index'))
user.add_url_rule('/login', endpoint='login', view_func=LoginView.as_view('login'))
