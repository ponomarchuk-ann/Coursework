from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from webapp.db import db
from webapp.news.views import blueprint as news_blueprint
from webapp.user.models import User
from webapp.user.views import blueprint as user_blueprint


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')

    db.init_app(app)
    # при первом запуске будет создана база данных
    with app.app_context():
        db.create_all()
    migrate = Migrate(app, db)

    app.register_blueprint(news_blueprint)
    app.register_blueprint(user_blueprint)

    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    return app
