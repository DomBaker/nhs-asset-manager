from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config, Secret
from flask_login import LoginManager, login_user, current_user, logout_user

database = SQLAlchemy()  # done here so that db is importable
login = LoginManager()


def create_app(config_class=Config, secret=Secret):
    app = Flask(__name__)
    app.config.from_object(config_class)
    database.init_app(app)
    login.init_app(app)
    return app
