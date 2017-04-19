#coding:utf-8

from flask import Blueprint, jsonify, request
from blog.models import Post, Category
from blog.tools import paginate, to_json
from blog.error import error_decorate


index_bp = Blueprint('index', __name__, url_prefix='/api/v1/index')


@index_bp.route('/article')
@error_decorate
def index():
    '''文章列表'''
    offset = request.args.get('offset', 1)  # 第几页
    limit = request.args.get('limit', 10)    # 返回几个
    return jsonify(paginate(Post.query, offset, limit, related=True))


@index_bp.route('/article/detailed')
@error_decorate
def article_detailed():
    '''文章详情'''
    offset = request.args.get('article_id', 1)
    query = Post.query.get(int(offset))
    if query is None:
        return jsonify({})
    else:
        return jsonify(to_json(query, related=True))


@index_bp.route('/category')
@error_decorate
def category():
    '''分类列表'''
    offset = request.args.get('offset', 1)  # 第几页
    limit = request.args.get('limit', 10)    # 返回几个
    return jsonify(paginate(Category.query, offset, limit))


@index_bp.route('/category/article')
@error_decorate
def category_article():
    '''单个分类列表'''
    category_id = request.args.get('category_id', '')
    offset = request.args.get('offset', 1)
    limit = request.args.get('limit', 10)
    query = Category.query.get(int(category_id))
    if query is not None:
        return jsonify(paginate(query.posts, offset, limit))
    else:
        return jsonify({})
