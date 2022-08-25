# -*- coding: utf-8 -*-
# @Time    : 2022/8/24 16:02
# @Author  : LZZ
# @FileName: mixin.py
# @Software: PyCharm
from flask_jwt_extended import jwt_required


class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, name):
        view = super(LoginRequiredMixin, cls).as_view(name)
        return jwt_required(view)

