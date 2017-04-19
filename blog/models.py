# coding=utf-8
from ext import db
from datetime import datetime
from werkzeug.security import generate_password_hash


class User(db.Model):
    '''user table'''
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True)
    password = db.Column(db.String(256))

    def __init__(self, username, password):
        self.username = username
        self.password = self.set_password(password)

    def set_password(self, password):
        '''设置生成密码'''
        return generate_password_hash(
            password,
            method='pbkdf2:sha256',
            salt_length=8
        )

    def __repr__(self):
        return self.username


class Post(db.Model):
    '''文章'''
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256), unique=True)
    body = db.Column(db.Text)
    created = db.Column(db.DateTime)
    updated = db.Column(db.DateTime)

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship(
        'Category',
        backref = db.backref('posts', lazy='dynamic')
    )

    def __init__(self, title, body, category, created=None, updated=None):
        self.title = title
        self.body = body
        if created is None:
            created = datetime.now()
        self.created = created
        if updated is None:
            updated = datetime.now()
        self.updated = updated
        self.category = category

    def __repr__(self):
        return self.title


class Category(db.Model):
    '''分类'''
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    created = db.Column(db.DateTime)
    updated = db.Column(db.DateTime)

    def __init__(self, name, created=None, updated=None):
        self.name = name
        if created is None:
            created = datetime.now()
        self.created = created
        if updated is None:
            updated = datetime.now()
        self.updated = updated

    def __repr__(self):
        return self.name

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'created': self.created,
            'updated': self.updated,
        }