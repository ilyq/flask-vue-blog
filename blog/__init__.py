# coding:utf-8

from flask import Flask
from flask_cors import CORS
from ext import db
from blog.error_msg import errors

# 导入数据模型
from blog.models import Post, User

app = Flask(__name__)
app.config.from_object('config')
db.init_app(app)
CORS(app)

with app.app_context():
    # db.drop_all()
    db.create_all()

# 导入视图
import blog.error

# 通过蓝图注册
import blog.admin
app.register_blueprint(blog.admin.admin_bp)
import blog.user
app.register_blueprint(blog.user.user_bp)
import blog.index
app.register_blueprint(blog.index.index_bp)
