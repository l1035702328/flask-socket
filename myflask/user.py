# -*- coding: utf-8 -*-
# @Time    : 2022/8/12 11:26
# @Author  : LZZ
# @FileName: user.py
# @Software: PyCharm

from flask import Blueprint
from flask.views import MethodView

user = Blueprint('user', __name__)


class Login(MethodView):
    def get(self):
        return "render_template('user.html')"

    def post(self):
        return "world"


user.add_url_rule('/', endpoint='login', view_func=Login.as_view('login'))
user.add_url_rule('/login', endpoint='login2', view_func=Login.as_view('login'))
