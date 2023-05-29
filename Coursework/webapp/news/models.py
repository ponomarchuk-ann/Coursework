"""
В данном файле описан класс новостей: в базе данных хранятся id новости, абсолютная ссылка на неё, заголовок новости
время чтения новости, дата публикации новости, а также текст новости
"""


from webapp.db import db


class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String, unique=True, nullable=False)
    title = db.Column(db.String, nullable=False)
    # поскольку время чтения - категориальный фильтр, то достаточно хранить его в виде одной буквы латинского
    # алфавита - S, если время чтения меньше пяти минут, M, если чтение занимает от пяти до десяти минут, и L,
    # если чтение занимает больше десяти минут
    read_time = db.Column(db.String(1), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    text = db.Column(db.Text)

    # функция позволяет получить время чтения для статьи, если оно не было получено с сайта, который мы парсили
    def get_read_time(self, value):
        if not value.isdigit():
            value = value.split()
            value = len(value) // 250
        value = int(value)
        if value < 5:
            self.read_time = 'S'
        elif value < 10:
            self.read_time = 'M'
        else:
            self.read_time = 'L'

    def __repr__(self):
        return f'Пост {self.id} - {self.title}'
