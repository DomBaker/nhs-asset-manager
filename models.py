from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

from app import database

# For some reason Heroku doesn't like imported versions of this so had to re-ref SQLAlchemy in this file.
database = SQLAlchemy()

#Using UserMixin for additional functionality
class User(UserMixin, database.Model):
    """ USER MODEL """

    __tablename__ = "users"
    id = database.Column(database.Integer, primary_key=True)
    email = database.Column(database.String(), unique=True, nullable=False)
    fname = database.Column(database.String(40), nullable=False)
    lname = database.Column(database.String(50), nullable=False)
    position = database.Column(database.String(), nullable=False)
    password = database.Column(database.String(), nullable=False)
    is_admin = database.Column(database.Boolean, nullable=False, default=False)

class Assets(database.Model):
    """ ASSET MODEL """

    __tablename__ = "assets"
    id = database.Column(database.Integer, primary_key=True)
    asset_name = database.Column(database.String(), nullable=False)
    owner_id = database.Column(database.Integer, database.ForeignKey('users.id'), nullable=True)
    asset_type = database.Column(database.String(), nullable=False)
    serial_number = database.Column(database.Integer, unique=True, nullable=False)

#database.create_all()

#database.drop_all()

