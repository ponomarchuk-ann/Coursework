"""
    В этом файле реализован парсинг сайта https://www.ixbt.com//
"""


from datetime import datetime
from webapp import create_app
import locale
import utils

# изменяем локаль, чтобы корректно считывать названия месяцев на русском языке
locale.setlocale(locale.LC_ALL, 'ru_RU.utf8')


def parse_ixbt(url):
    print('Начал парсить...')
    soup = utils.get_soup(url)
    posts = soup.find_all(
        'article',
        class_='col-md-4 topic topic-thumbnail topic-type-topic',
        )
    for post in posts:
        title = post.find('h3').text
        url = post.find('h3').find('a')['href']
        # изменяем дату: по умолчанию год не указан и равен 1900
        time_str = '2023 ' + post.find('time')['title']
        parsed_datetime = datetime.strptime(time_str, '%Y %d %B, %H:%M')

        soup2 = utils.get_soup(url)
        text = soup2.find('div', class_='topic-content text')

        utils.save_news(url, title, text.text, parsed_datetime, text)


if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        parse_ixbt('https://www.ixbt.com/live/blog/sw/')
        parse_ixbt('https://www.ixbt.com/live/blog/platform')
        parse_ixbt('https://www.ixbt.com/live/blog/mobilepc')
        parse_ixbt('https://www.ixbt.com/live/blog/mobile')
