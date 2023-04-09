from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import check_password_hash

from db.orm_db import sqlite_db
from login.manager import login_manager


@login_manager.user_loader  # 定义获取登录用户的方法
def load_user(user_id):
    return User.get(user_id)


class User(sqlite_db.Model, UserMixin):
    id = sqlite_db.Column(sqlite_db.Text, primary_key=True)
    username = sqlite_db.Column(sqlite_db.Text, nullable=False)
    password = sqlite_db.Column(sqlite_db.Text, nullable=False)
    create_time = sqlite_db.Column(sqlite_db.DateTime, nullable=False, default=datetime.now())
    activate = sqlite_db.Column(sqlite_db.Boolean, nullable=False, default=True)
    time_to_activate = sqlite_db.Column(sqlite_db.DateTime, nullable=True)

    def get_id(self):
        """获取用户ID"""
        return self.id

    def verify_password(self, password):
        # 明文密码
        return check_password_hash(self.password, password)

    @staticmethod
    def get(user_id):
        """根据用户ID获取用户实体，为 login_user 方法提供支持"""
        if not user_id:
            return None
        try:
            user_from_model = User.query.filter_by(id=user_id).first()
            if not user_from_model:
                return None
            else:
                return user_from_model
        except Exception as e:
            print(e.__str__())
            return None


class Layer(sqlite_db.Model):
    id = sqlite_db.Column(sqlite_db.Integer, primary_key=True, autoincrement=True)
    layer_name = sqlite_db.Column(sqlite_db.Text, nullable=False, unique=True)


class Part(sqlite_db.Model):
    id = sqlite_db.Column(sqlite_db.Integer, primary_key=True, autoincrement=True)
    layer_id = sqlite_db.Column(sqlite_db.Integer, sqlite_db.ForeignKey('layer.id'))
    part_name = sqlite_db.Column(sqlite_db.Text, nullable=False)


class Desk(sqlite_db.Model):
    id = sqlite_db.Column(sqlite_db.Integer, primary_key=True, autoincrement=True)
    part_id = sqlite_db.Column(sqlite_db.Integer, sqlite_db.ForeignKey('part.id'))
    desk_name = sqlite_db.Column(sqlite_db.Text, nullable=False)


class Stool(sqlite_db.Model):
    id = sqlite_db.Column(sqlite_db.Integer, primary_key=True, autoincrement=True)
    desk_id = sqlite_db.Column(sqlite_db.Integer, sqlite_db.ForeignKey('desk.id'))
    stool_name = sqlite_db.Column(sqlite_db.Text, nullable=False)


class Appoint(sqlite_db.Model):
    id = sqlite_db.Column(sqlite_db.Integer, primary_key=True, autoincrement=True)
    user_id = sqlite_db.Column(sqlite_db.Text, sqlite_db.ForeignKey('user.id'), nullable=False)
    stool_id = sqlite_db.Column(sqlite_db.Integer, sqlite_db.ForeignKey('stool.id'), nullable=False)
    create_time = sqlite_db.Column(sqlite_db.DateTime, nullable=False, default=datetime.now())


class Book(sqlite_db.Model):
    id = sqlite_db.Column(sqlite_db.Integer, primary_key=True, autoincrement=True)
    # 书名
    book_name = sqlite_db.Column(sqlite_db.Text, nullable=False)
    # 作者
    author = sqlite_db.Column(sqlite_db.Text, nullable=True)
    # 翻译人
    translator = sqlite_db.Column(sqlite_db.Text, nullable=True)
    # ISBN
    isbn = sqlite_db.Column(sqlite_db.Text, nullable=True)
    # 作者介绍
    author_introduction = sqlite_db.Column(sqlite_db.Text, nullable=True)
    # 种类
    catalog = sqlite_db.Column(sqlite_db.Text, nullable=True)
    # 出版社
    publisher = sqlite_db.Column(sqlite_db.Text, nullable=True)
    # 介绍
    abstract = sqlite_db.Column(sqlite_db.Text, nullable=True)
    # 图片
    picture = sqlite_db.Column(sqlite_db.Text, nullable=True)


class Borrow(sqlite_db.Model):
    id = sqlite_db.Column(sqlite_db.Integer, primary_key=True, autoincrement=True)
    book_id = sqlite_db.Column(sqlite_db.Integer, sqlite_db.ForeignKey('book.id'), nullable=False)
    user_id = sqlite_db.Column(sqlite_db.Text, sqlite_db.ForeignKey('user.id'), nullable=False)
    create_time = sqlite_db.Column(sqlite_db.DateTime, nullable=False, default=datetime.now())


class Admin(sqlite_db.Model, UserMixin):
    id = sqlite_db.Column(sqlite_db.Text, primary_key=True)
    username = sqlite_db.Column(sqlite_db.Text, nullable=False)
    password = sqlite_db.Column(sqlite_db.Text, nullable=False)
    create_time = sqlite_db.Column(sqlite_db.DateTime, nullable=False, default=datetime.now())

    def get_id(self):
        """获取用户ID"""
        return self.id

    def verify_password(self, password):
        # 明文密码
        return check_password_hash(self.password, password)

    @staticmethod
    def get(user_id):
        """根据用户ID获取用户实体，为 login_user 方法提供支持"""
        if not user_id:
            return None
        try:
            user_from_model = Admin.query.filter_by(id=user_id).first()
            if not user_from_model:
                return None
            else:
                return user_from_model
        except Exception as e:
            print(e.__str__())
            return None
