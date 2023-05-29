"""
    В этом файле реализован парсинг сайта https://telecomdaily.ru/
"""

from bs4 import BeautifulSoup
from datetime import datetime
from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.chrome.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from webapp import create_app
import locale
import os
import time
import utils

# изменяем локаль, чтобы корректно считывать названия месяцев на русском языке
locale.setlocale(locale.LC_ALL, 'ru_RU.utf8')


def get_driver():
    options = Options()
    options.add_argument('--no-sandbox')
    driver = webdriver.Firefox(
        service=Service(os.path.join(os.getcwd(), 'geckodriver')),
        options=options,
    )
    return driver


def parse_telecom(url):
    print('Начал парсить...')
    driver = get_driver()
    driver.get(url)
    # даём сайту время прогрузиться - двух секунд будет достаточно
    time.sleep(2)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    posts = soup.find_all('div', class_='news-teaser')
    for post in posts:
        title = post.find('a').text
        # заменяем относительную ссылку на новость на абсолютную
        url = 'https://telecomdaily.ru' + post.find('a')['href']
        # изменяем дату: по умолчанию год не указан и равен 1900
        date = '2023 ' + post.find('div', class_='created-at').text
        date = datetime.strptime(date, '%Y %d %B %H.%M')
        driver.get(url)
        # даём сайту время прогрузиться - двух секунд будет достаточно
        time.sleep(2)
        html = driver.page_source
        soup2 = BeautifulSoup(html, 'html.parser')
        text = soup2.find('div', class_='news-item')

        # избавляемся от ненужных частей html-документа: рекламных баннеров, кликабельных иконок социальных сетей и прочего
        soup = BeautifulSoup(text.decode_contents(), 'html.parser')
        div_tag = soup.find('div', class_='share-container-wrapper')
        if div_tag:
            div_tag.extract()
        div_tag = soup.find('div', class_='megabitus')
        if div_tag:
            div_tag.extract()
        div_tag = soup.find('div', class_='rubrics')
        if div_tag:
                div_tag.extract()
        div_tag = soup.find('div', class_='tags')
        if div_tag:
            div_tag.extract()
        div_tag = soup.find('div', class_='main-tag')
        if div_tag:
            div_tag.extract()
        div_tag = soup.find('div', class_='title')
        if div_tag:
            div_tag.extract()

        utils.save_news(url, title, text.text, date, soup)


if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        parse_telecom('https://telecomdaily.ru/rubric/science')
