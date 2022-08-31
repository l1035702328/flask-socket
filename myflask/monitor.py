# -*- coding: utf-8 -*-
# @Time    : 2022/8/26 18:22
# @Author  : LZZ
# @FileName: monitor.py
# @Software: PyCharm

from flask import Blueprint, jsonify, request
from flask.views import MethodView
from flask_jwt_extended import create_access_token, get_jwt_identity, create_refresh_token, get_jwt_claims
from myflask.models import User
from myflask.result_msg import make_response_success, make_response_400
from utils.mixin import LoginRequiredMixin

monitor = Blueprint('monitor_view', __name__)

class RealMonitor(LoginRequiredMixin,MethodView):
    def get(self):
        # 获取redis实时数据

        return "hello"

monitor.add_url_rule('/', endpoint='index', view_func=RealMonitor.as_view('index'))

