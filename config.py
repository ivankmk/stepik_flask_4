import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'my-secret-key'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(
        basedir, 'db.db'
        )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    FLASK_ENV = 'development'
