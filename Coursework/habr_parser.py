"""
    В этом файле реализован парсинг сайта https://habr.com/
"""

from bs4 import BeautifulSoup
from datetime import datetime
from webapp import create_app
import utils


def parse_habr(url):
    print('Начал парсить...')
    soup = utils.get_soup(url)
    posts = soup.find_all('article', class_='tm-articles-list__item')
    for post in posts:
        title = post.find('h2')
        # заменяем относительную ссылку на новость на абсолютную
        url = 'https://habr.com' + title.find('a')['href']
        title = title.text
        # считываем время чтения, указанное на сайте
        read_time = post.find('span', class_='tm-article-reading-time__label').text.strip().split()[0]
        date = post.find('span', class_='tm-article-datetime-published').find('time')['title']
        date = datetime.strptime(date, '%Y-%m-%d, %H:%M')
        soup2 = utils.get_soup(url)
        text = soup2.find('div', class_='tm-article-presenter__body')

        # избавляемся от ненужных частей html-документа: рекламных баннеров, кликабельных иконок социальных сетей и прочего
        soup = BeautifulSoup(text.decode_contents(), 'html.parser')
        div_tag = soup.find('span', class_="tm-article-complexity__label")
        if div_tag:
            div_tag.extract()
        div_tag = soup.find('div', class_='tm-separated-list tm-article-presenter__meta-list')
        if div_tag:
            div_tag.extract()
        div_tag_to_delete = soup.find('div', class_='tm-data-icons tm-article-sticky-panel__icons')
        if div_tag_to_delete:
            div_tag_to_delete.extract()
        tag_to_delete = soup.find('a', class_='tm-user-info__userpic')
        if tag_to_delete:
            tag_to_delete.extract()
        tag_to_delete = soup.find('span', class_='tm-icon-counter tm-data-icons__item')
        if tag_to_delete:
            tag_to_delete.extract()
        div_tag_to_delete = soup.find('div', class_='tm-article-presenter__meta')
        if div_tag_to_delete:
            div_tag_to_delete.extract()
        div_tag_to_delete = soup.find('span', class_='tm-article-datetime-published')
        if div_tag_to_delete:
            div_tag_to_delete.extract()
        elements = soup.find_all(class_='tm-article-snippet__hubs-item-link')
        for element in elements:
            element["href"] = url

        utils.save_news(url, title, read_time, date, soup)


if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        parse_habr('https://habr.com/ru/news/')
