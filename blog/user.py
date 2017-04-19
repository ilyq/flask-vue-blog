# coding:utf-8

from flask import Blueprint, jsonify, request
from blog.error import error_decorate
from blog.exception import ParameterException, UsernameException, LoginException
from blog.models import User
from blog.ext import db
from werkzeug.security import check_password_hash
from blog.tools import get_random_token
from blog.auth import auth_list


user_bp = Blueprint('user', __name__, url_prefix='/api/v1/user')


def check_password(pw_hash, password):
    '''验证密码'''
    return check_password_hash(pw_hash, password)


def login(username, password):
    '''登录'''
    doc = User.query.filter_by(username=username).first()
    if not doc:
        raise LoginException('username error')

    if not check_password(doc.password, password):
        raise LoginException('password error')

    token = get_random_token()

    auth_list.login = token
    print(auth_list.login)

    login_data = {
        'username': username,
        'token': token,
        'expires': 7200
    }
    return login_data


@user_bp.route('/register', methods=['POST'])
@error_decorate
def register():
    '''注册'''
    if request.method == 'POST':
        username = request.json.get('username')
        password = request.json.get('password')

        if not username:
            raise ParameterException('username parameter error')

        if not password:
            raise ParameterException('password parameter error')

        assert 4 <= len(username) <= 32, (102, u'用户名长度必须在2 ~ 32')
        assert 4 <= len(password) <= 256, (103, u'密码长度必须在6 ~ 100')

        doc = User.query.filter_by(username=username).first()
        if doc:
            raise UsernameException('username is save')

        admin = User(username, password)
        db.session.add(admin)
        db.session.commit()

        return jsonify(login(username, password))


@user_bp.route('/login', methods=['POST'])
@error_decorate
def user_login():
    '''登录'''
    if request.method == 'POST':
        username = request.json.get('username')
        password = request.json.get('password')

        if not username:
            raise ParameterException('username parameter error')

        if not password:
            raise ParameterException('password parameter error')

        return jsonify(login(username, password))
