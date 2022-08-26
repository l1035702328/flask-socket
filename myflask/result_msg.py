# -*- coding: utf-8 -*-
# @Time    : 2022/8/26 16:29
# @Author  : LZZ
# @FileName: result_msg.py
# @Software: PyCharm

from flask import make_response, jsonify

def response_success_data(qts_data):
    return {
        'qts_result':True,
        'qts_haserr':False,
        'qts_msg':None,
        'qts_data':qts_data
    }

def response_error_data(qts_msg):
    return {
        'qts_result': False,
        'qts_haserr': True,
        'qts_msg': qts_msg,
        'qts_data': None
    }

def make_response_success(qts_data):
    return make_response(jsonify(response_success_data(qts_data)), 200)

def make_response_400():
    return make_response(jsonify(response_error_data('请求无效')), 400)

def make_response_401():
    return make_response(jsonify(response_error_data('权限不足')), 401)

def make_response_403():
    return make_response(jsonify(response_error_data('禁止访问')), 401)

def make_response_404():
    return make_response(jsonify(response_error_data('请求不存在')), 404)

def make_response_500(e):
    return make_response(jsonify(response_error_data(e)), 500)
