# -*- coding: utf-8 -*-
# @Time    : 2022/8/12 11:26
# @Author  : LZZ
# @FileName: view.py
# @Software: PyCharm

from flask import Blueprint
from flask.views import MethodView

index = Blueprint('index', __name__)


class MyView(MethodView):
    def get(self):
        return "render_template('index.html')"

    def post(self):
        return "world"

index.add_url_rule('/', endpoint='login', view_func=MyView.as_view('login'))
# @index.route('/')
# def show():
#     return 'app02.hello'