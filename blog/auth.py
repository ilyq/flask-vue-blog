# coding:utf-8

import logging
from functools import wraps
from flask import request, jsonify
from blog.exception import NoLoginException, TokenException


def is_authenticated(func):
    '''登录认证'''
    @wraps(func)
    def wrapped(*args, **kwargs):
        try:
            if request.args.get('token'):
                if request.args.get('token') in auth_list.login:
                    return func(*args, **kwargs)
                else:
                    raise TokenException('token invalid')
            else:
                raise NoLoginException('not login')
        except Exception as e:
            logging.error(e)
            if isinstance(e, NoLoginException):
                code = 108
                msg = e.args[0]
            elif isinstance(e, TokenException):
                code = 109
                msg = e.args[0]
            data = {
                'code': code,
                'msg': msg
            }
            return jsonify(data)

    return wrapped


class AuthList(object):

    def __init__(self):
        self.login_list = []

    @property
    def login(self):
        return self.login_list

    @login.setter
    def login(self, value):
        self.login_list.append(value)


auth_list = AuthList()
