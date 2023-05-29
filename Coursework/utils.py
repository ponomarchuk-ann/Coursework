"""
    В этом файле реализованы две ключевые функции для парсинга сайтов, которые будут запущены из, собственно, парсеров
"""


from bs4 import BeautifulSoup
from webapp.db import db
from webapp.news.models import News
import requests

# получаем html код сайта, проверяя в первую очередь, что он доступен на текущий момент
def get_soup(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return BeautifulSoup(response.text, 'html.parser')
    except requests.RequestException:
        return False


# если новость ещё не была добавлена в базу данных, сохраняем заголовок новости, ссылку на неё, дату публикации,
# а также текст новости в формате html-документа, в котором корректируем относительные ссылки на авторов,
# заменяя их на абсолютные
def save_news(url, title, read_time, date, text):
    check_news = News.query.filter(News.url == url).count()
    if not check_news:
        text = text.decode_contents()
        text = text.replace('href="/ru/users/', 'href="https://habr.com/ru/users/')
        text = text.replace('href="/author/', 'href="https://telecomdaily.ru/author/')
        new_post = News(
            url=url,
            title=title,
            date=date,
            text=text,
        )
        new_post.get_read_time(read_time)
        db.session.add(new_post)
        db.session.commit()
