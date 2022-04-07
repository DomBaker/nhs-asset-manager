from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

from app import app, database

# For some reason Heroku doesn't like imported versions of this so had to re-ref SQLAlchemy in this file
# I'm guessing this may have something to do with gunicorn also.
#database = SQLAlchemy()

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

    # def __init__(self, asset_name: str, asset_type: str, serial_number: int):
    #     self.asset_name = asset_name
    #     self.asset_type = asset_type
    #     self.serial_number = serial_number


#you will need to uncomment database.creat_all() to create a db locally, you will also need to set the export for DATABASE to your
# database uri    

#database.create_all()

#database.drop_all()

