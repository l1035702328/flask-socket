# -*- coding: utf-8 -*-
# @Time    : 2022/8/26 10:02
# @Author  : LZZ
# @FileName: admin.py
# @Software: PyCharm
import flask_jwt_extended
from flask import url_for, request
from flask_admin import expose, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_jwt_extended import get_jwt_claims, get_jwt_identity, verify_jwt_in_request
from werkzeug.utils import redirect

from utils.mixin import LoginRequiredMixin


# class MyUserView(ModelView):
#     def is_accessible(self):
#         current_identity = verify_jwt_in_request()
#         print(current_identity)
#         claims = get_jwt_claims()
#         if claims:
#             if claims['role'] == 'admin':
#                 print("允许访问")
#                 return True
#             else:
#                 print("无权限")
#                 print(claims['role'])
#                 return False
#         print("未登录")
#         return False
#
#     def inaccessible_callback(self, name, **kwargs):
#         # redirect to login page if user doesn't have access
#         return redirect(url_for('user_view.login', next=request.url))
#
#
# class MyAdminIndexView(AdminIndexView):
#     @expose('/')
#     def index(self):
#         current_identity = get_jwt_identity()
#         print(current_identity)
#         if 1:
#             return super(MyAdminIndexView, self).index()
#         return redirect(url_for('user_view.login'))
#
#
