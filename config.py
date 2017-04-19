# coding:utf-8

DEBUG = True

HOSTNMAE = 'localhost'
DATABASE = 'r'
USERNAME = 'web'
PASSWORD = 'web'

# MYSQL
# mysql://username:password@server/db
# DB_URI = 'mysql://{}:{}@{}/{}'.format(
#     USERNAME, PASSWORD, HOSTNMAE, DATABASE
# )

# SQLITE
# ///代表当前位置
DB_URI = 'sqlite:///../web.db'

SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_ECHO = False
SQLALCHEMY_TRACK_MODIFICATIONS = False
