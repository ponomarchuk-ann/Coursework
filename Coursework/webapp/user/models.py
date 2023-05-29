"""
В данном файле описаны два класса, связанных с пользователей - сам пользователь (в базе данных хранятся его id, имя
пользователя, а также пароль) и его избранные новости (они привязаны к таблице пользователей и новостей)
"""

from flask_login import UserMixin
from webapp.db import db
from werkzeug.security import check_password_hash, generate_password_hash


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    # проверка совпадения пароля с сохранённым в системе
    def check_password(self, password):
        return check_password_hash(self.password, password)

    # запоминание введённого пароля
    def set_password(self, password):
        self.password = generate_password_hash(password)


class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id', ondelete='CASCADE'),
    )
    news_id = db.Column(
        db.Integer,
        db.ForeignKey('news.id', ondelete='CASCADE'),
    )
