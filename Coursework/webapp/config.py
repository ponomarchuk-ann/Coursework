import os

SECRET_KEY = 'your_secret_key'
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(os.getcwd(), 'news.db')
