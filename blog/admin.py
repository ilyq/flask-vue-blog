# coding:utf-8

from flask import Blueprint, jsonify, request
from blog.auth import is_authenticated
from blog.models import Category, Post
from blog.ext import db
from blog.exception import ParameterException, DataAlreadyExistsException, DataDoesNotExistException
from blog.error import error_decorate
from blog.tools import to_json, paginate


admin_bp = Blueprint('admin', __name__, url_prefix='/api/v1/admin')


@admin_bp.route('/index', methods=['POST'])
@error_decorate
@is_authenticated
def index():
    '''admin index
    http://127.0.0.1:5000/api/v1/admin/index?token=ebcf19852dec49deab52f0f468df0077
    '''
    if request.method == 'POST':
        data = {
            'msg': 'admin index'
        }
        return jsonify(data)


@admin_bp.route('/verify/token', methods=['GET'])
@error_decorate
@is_authenticated
def verify_token():
    '''verify token'''
    data = {
        'msg': 'verify success'
    }
    return jsonify(data)


@admin_bp.route('/category', methods=['GET', 'POST', 'PUT', 'DELETE'])
@error_decorate
@is_authenticated
def category():
    if request.method == 'GET':
        offset = request.args.get('page', 1)  # 第几页
        limit = request.args.get('per_page', 10)  # 返回几个
        return jsonify(paginate(Category.query, offset, limit))
    elif request.method == 'POST':
        # 创建
        name = request.get_json().get('name')
        if name is None:
            raise ParameterException('name parameter error')
        query = Category.query.filter_by(name=name).first()
        if query is None:
            doc = Category(name)
            db.session.add(doc)
            db.session.commit()
            data = {
                'msg': 'created success'
            }
            return jsonify(data)
        else:
            raise DataAlreadyExistsException('Data already exists')
    elif request.method == 'PUT':
        # 更新
        # rows_changed = User.query.filter_by(role == 'admin').update(dict(permission='add_user'))
        # db.session.commit()
        name = request.get_json().get('name')
        new_name = request.get_json().get('new_name')
        if name is None:
            raise ParameterException('name parameter error')
        query = Category.query.filter_by(name=name).first()
        if query is not None:
            query.name = new_name
            db.session.commit()
            data = {
                'msg': 'update success'
            }
            return jsonify(data)
        else:
            raise DataDoesNotExistException('Data does not exist')
    elif request.method == 'DELETE':
        # 删除
        name = request.get_json().get('name')
        if name is None:
            raise ParameterException('name parameter error')
        query = Category.query.filter_by(name=name).first()
        if query is not None:
            db.session.delete(query)
            db.session.commit()
            data = {
                'msg': 'delete success'
            }
            return jsonify(data)
        else:
            raise DataDoesNotExistException('Data does not exist')


@admin_bp.route('/article', methods=['GET', 'POST', 'PUT', 'DELETE'])
@is_authenticated
@error_decorate
def article():
    if request.method == 'GET':
        offset = request.args.get('page', 1)  # 第几页
        limit = request.args.get('per_page', 10)    # 返回几个
        return jsonify(paginate(Post.query, offset, limit, related=True))
    elif request.method == 'POST':
        request_data = request.get_json()
        print(request_data)

        category_query = Category.query.filter_by(name=request_data.get('category')).first()
        if category_query is None:
            raise ParameterException("category: error")

        title_query = Post.query.filter_by(title=request_data.get('title')).first()
        if title_query is not None:
            raise ParameterException("title: error")

        if request_data.get("title") is None or request_data.get('body') is None:
            raise ParameterException("parameter error")

        doc = Post(
            title=request_data.get('title'),
            body=request_data.get('body'),
            category=category_query
        )
        db.session.add(doc)
        db.session.commit()
        return jsonify(to_json(doc))
    elif request.method == 'PUT':
        request_data = request.get_json()

        category_query = Category.query.filter_by(name=request_data.get('category')).first()
        if category_query is None:
            raise ParameterException("category: error")

        if request_data.get("title") is None or request_data.get('body') is None or request_data.get('id') is None:
            raise ParameterException("parameter error")

        article_query = Post.query.get(request_data.get('id'))
        if article_query is None:
            data_err = {
                'errmsg': 'update failed'
            }
            return jsonify(data_err)
        else:
            article_query.title = request_data.get('title')
            article_query.body = request_data.get('body')
            article_query.category = category_query

        db.session.commit()
        return jsonify(to_json(Post.query.get(request_data.get('id'))))
    elif request.method == 'DELETE':
        article_id = request.get_json().get('id')
        if article_id is None:
            raise ParameterException('id: error')
        query = Post.query.get(article_id)
        if query is None:
            data_err = {
                'errmsg': 'delete failed'
            }
            return jsonify(data_err)
        else:
            db.session.delete(query)
            db.session.commit()
            data = {
                "msg": 'delete success'
            }
            return jsonify(data)
