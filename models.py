from sqlite3 import sqlite_version_info
from urllib.request import DataHandler
from flask_sqlalchemy import SQLAlchemy

database = SQLAlchemy()

class User(database.Model):
    """ USER MODEL """

    __tablename__ = "users"
    id = database.Column(database.Integer, primary_key=True)
    email = database.Column(database.String(30), unique=True, nullable=False)
    password = database.Column(database.String(), nullable=False)




