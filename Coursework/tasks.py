"""
    В этом файле реализована логика автоматического парсинга новостей: новости со всех страниц парсятся
    раз в минуту, благодаря чему на сайт почти моментально попадают только что опубликованные новости
"""

from celery import Celery
from celery.schedules import crontab
from webapp import create_app
import habr_parser as habr_parser
import ixbt_parser as ixbt_parser
import telecom_parser as telecom_parser

# указываем локальный порт, который занимает redis; узнать его можно при помощи команды redis-server
celery_app = Celery('tasks', broker='redis://127.0.0.1:6381/0')
flask_app = create_app()


# создаём задание для Celery
@celery_app.task
def parse_news():
    with flask_app.app_context():
        habr_parser.parse_habr('https://habr.com/ru/hub/python/top/weekly/')
        ixbt_parser.parse_ixbt('https://www.ixbt.com/live/blog/sw/')
        ixbt_parser.parse_ixbt('https://www.ixbt.com/live/blog/platform')
        ixbt_parser.parse_ixbt('https://www.ixbt.com/live/blog/mobilepc')
        ixbt_parser.parse_ixbt('https://www.ixbt.com/live/blog/mobile')
        telecom_parser.parse_telecom('https://telecomdaily.ru/rubric/science')


# добавляем задания в очередь - каждую минуту парсим шесть страниц
@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(crontab(minute='*/1'), parse_news.s())
