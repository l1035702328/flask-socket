# -*- coding: utf-8 -*-
# @Time    : 2022/8/12 11:26
# @Author  : LZZ
# @FileName: user.py
# @Software: PyCharm

from flask import Blueprint, jsonify, request
from flask.views import MethodView
from flask_jwt_extended import create_access_token, get_jwt_identity, create_refresh_token, get_jwt_claims
from myflask.models import User
from myflask.result_msg import make_response_success, make_response_400
from utils.mixin import LoginRequiredMixin

user = Blueprint('user_view', __name__)


class LoginView(MethodView):
    def get(self):
        return "please login"

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
                print("登录成功")
                additional_claims = {'role': user.role.name}
                access_token = create_access_token(identity=username, user_claims=additional_claims)
                refresh_token = create_refresh_token(identity="username",user_claims=additional_claims)
                res = {
                    'access_token': access_token,
                    'refresh_token': refresh_token
                }
                return make_response_success(res)
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
        current_identity = get_jwt_identity()
        print(current_identity)
        claims = get_jwt_claims()
        print("role:{}".format(claims['role']))
        return "hello this is index"

# jwt 刷新置换
class RefreshView(MethodView):
    def get(self):
        current_identity = get_jwt_identity()
        claims = get_jwt_claims()
        if current_identity:
            access_token = create_access_token(identity=current_identity, user_claims=claims)
            return jsonify(access_token= access_token),200

        return make_response_400()
# endpoint通常用来“反向查找”。例如，你想从一个页面跳转到另一个页面时，你可以使用url_for(endpoint,**values)
user.add_url_rule('/', endpoint='index', view_func=IndexView.as_view('index'))
user.add_url_rule('/login', endpoint='login', view_func=LoginView.as_view('login'))
user.add_url_rule('/refresh', endpoint='refresh', view_func=RefreshView.as_view('refresh'))
