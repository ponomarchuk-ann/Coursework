"""
В данном файле реализованы основные функции, связанные с работой с пользователем: регистрация пользователя,
авторизация пользователя, выход из аккаунта, добавление новости в избранное, а также отображение всех новостей,
добавленных в избранное
"""

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_user, logout_user
from webapp.db import db
from webapp.news.models import News
from webapp.user.forms import LoginForm, RegistrationForm
from webapp.user.models import Favorite, User

blueprint = Blueprint('user', __name__)


@blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    # проверка корректности заполнения формы для регистрации пользователя: совпадения пароля в полях "password" и
    # "confirm_password", а также уникальности имени пользователя
    if form.validate_on_submit():
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user:
            flash('Такое имя пользователя занято')
            return redirect(url_for('user.register'))
        new_user = User(username=form.username.data)
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()
        # flash('Регистрация прошла успешно!')
        return redirect(url_for('user.login'))
    flash('Пароли не совпадают!')
    # отрисовка нужно страницы на сайте
    return render_template('register.html', form=form, title='Регистрация')


@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if not current_user.is_anonymous:
        return redirect(url_for('news.index'))
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        remember_me = form.remember_me.data

        user = User.query.filter_by(username=username).first()
        # проверка совпадения введённого имени пользователя и пароля, сохранённых в базе данных
        if user and user.check_password(password):
            # flash('Авторизация прошла успешно')
            login_user(user, remember=remember_me)
            return redirect(url_for('news.index'))
        flash('Неверное имя пользователя или пароль')
    return render_template('login.html', form=form)


@blueprint.route('/logout')
def logout():
    # выход из аккаунта пользователя
    if current_user.is_anonymous:
        return redirect(url_for('news.index'))
    logout_user()
    return redirect(url_for('news.index'))


@blueprint.route('/add_to_favorites/<int:news_id>')
def add_to_favorites(news_id):
    # проверка, вошёл ли пользователь в свой аккаунт - функция добавления в избранное доступна только авторизованным
    # пользователям
    if current_user.is_anonymous:
        return redirect(url_for('user.login'))

    check_fav = Favorite.query.filter(Favorite.user_id == current_user.id).filter(Favorite.news_id == news_id).first()
    # если пользователь уже добавлял новость в избранное - значит, он хочет её удалить из избранного, реализуем это
    if check_fav:
        db.session.delete(check_fav)
        db.session.commit()
        # flash('Страница успешно удалена из избранного!')
    # иначе добавляем новость в избранное
    else:
        favorite = Favorite(
            user_id=current_user.id,
            news_id=news_id,
        )
        db.session.add(favorite)
        db.session.commit()
        # flash('Страница успешно добавлена в избранное!')
    if 'fav' in request.referrer:
        return redirect(url_for('user.favorites'))
    return redirect(url_for('news.index'))


@blueprint.route('/favorites')
def favorites():
    # просмотр всех новостей, добавленных пользователем в избранное
    favorites = Favorite.query.filter(Favorite.user_id == current_user.id).all()
    posts = News.query.all()
    news = []
    for f in favorites:
        news.append(f.news_id)
    return render_template('favorites.html', posts=posts, favs=news)
