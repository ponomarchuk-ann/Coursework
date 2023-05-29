"""
В данном файле реализованы основные функции, связанные с новостями: отображение всех новостей на главное странице,
отображение выбранной новости, категориальный фильтр по времени чтения новости
"""


from flask import Blueprint, abort, redirect, render_template, url_for
from flask_login import current_user
from webapp.news.models import News
from webapp.user.models import Favorite

blueprint = Blueprint('news', __name__)


@blueprint.route('/', )
def index():
    title = 'Новости'
    sorted_news = News.query.order_by(News.date.desc()).all()
    news = []
    if current_user.is_authenticated:
        favs_news = Favorite.query.filter(Favorite.user_id == current_user.id)
        for n in favs_news:
            news.append(n.news_id)
    return render_template(
        'index.html',
        title=title,
        posts=sorted_news,
        favs=news,
    )


@blueprint.route('/news/<int:news_id>')
def news_index(news_id):
    news = News.query.get(news_id)
    if not news:
        abort(404)
    return render_template(
        'news.html',
        news=news,
    )


@blueprint.route('/<int:read_time>')
def filter_by_read_time(read_time):
    title = 'Новости'
    if read_time == 0:
        return redirect(url_for('news.index'))
    match_ = {5: 'S', 10: 'M', 20: 'L'}
    posts = News.query.filter(News.read_time == match_[read_time]).order_by(News.date.desc()).all()
    news = []
    if current_user.is_authenticated:
        favs_news = Favorite.query.filter(Favorite.user_id == current_user.id)
        for n in favs_news:
            news.append(n.news_id)
    print(news)
    return render_template(
        'index.html',
        title=title,
        posts=posts,
        favs=news,
    )
