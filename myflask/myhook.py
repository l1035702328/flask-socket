# -*- coding: utf-8 -*-
# @Time    : 2022/8/26 12:58
# @Author  : LZZ
# @FileName: myhook.py
# @Software: PyCharm
import flask_jwt_extended
import jwt
from flask import request
from flask_jwt_extended import get_jwt_identity, get_jwt_claims, get_raw_jwt, jwt_required
import re
import config


def sys_before_request():
    admin_re = re.compile('/admin.*')
    print(request.path)
    print("钩子")
    if admin_re.match(request.path):
        try:
            token = request.headers.get("Authorization")
            token = re.match(r"Bearer (.*)", token).group(1)
            print(token)
            unverified_claims = flask_jwt_extended.decode_token(token)
            # unverified_claims = jwt.decode(jwt=token, algorithms=['HS256'], key=config.Config.JWT_SECRET_KEY)
            user_claims = unverified_claims.get('user_claims')
            identity = unverified_claims.get('identity')
            if user_claims['role'] == 'admin':
                print("有权限访问")
                pass
            else:
                return "无权限访问"
        except Exception as e:
            print(e)
            return "异常"

