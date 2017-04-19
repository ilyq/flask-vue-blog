# coding:utf-8

import logging
import traceback
from functools import wraps
from flask import jsonify
from blog import app
from flask.wrappers import BadRequest
from blog.exception import ParameterException, \
    UsernameException, \
    LoginException, \
    DataAlreadyExistsException, \
    DataDoesNotExistException
from sqlalchemy.exc import IntegrityError


@app.errorhandler(404)
def page_not_found(error):
    data = {
        'error': 'page not found'
    }
    return jsonify(data), 404


@app.errorhandler(403)
def forbidden(error):
    data = {
        'error': 'Forbidden'
    }
    return jsonify(data), 403

@app.errorhandler(405)
def method_not_allowed(error):
    data = {
        'error': '请求失败'
    }
    return jsonify(data), 405


@app.errorhandler(500)
def internal_server_error(error):
    data = {
        'error': 'Internal Server Error'
    }
    return jsonify(data), 500


def error_decorate(func):
    '''错误装饰器'''

    @wraps(func)
    def wrapped(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logging.error(e)
            logging.error(traceback.format_exc())
            if isinstance(e, AssertionError):
                code, msg = e.args[0]
            elif isinstance(e, ParameterException):
                code = 101
                msg = e.args[0]
            elif isinstance(e, (ValueError, AttributeError, BadRequest, TypeError)):
                code = 104
                msg = u'服务器内部错误'
            elif isinstance(e, IntegrityError):
                code = 105
                msg = u'数据库操作错误'
            elif isinstance(e, UsernameException):
                code = 106
                msg = e.args[0]
            elif isinstance(e, LoginException):
                code = 107
                msg = e.args[0]
            elif isinstance(e, DataAlreadyExistsException):
                code = 110
                msg = e.args[0]
            elif isinstance(e, DataDoesNotExistException):
                code = 111
                msg = e.args[0]
            else:
                code = 999
                msg = u'未知错误'
            data_err = {
                'errcode': code,
                'errmsg': msg
            }
            return jsonify(data_err)
    return wrapped
