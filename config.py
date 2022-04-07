import os
class Config:
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE")

class Secret:
    SECRET = os.environ.get('SECRET_KEY')
