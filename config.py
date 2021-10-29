from os import environ, path
from dotenv import load_dotenv
import redis

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, 'cfg.env'))


class Config:

    # Flask
    FLASK_APP = 'wsgi.py'
    SECRET_KEY = environ.get('SECRET_KEY')

    # Flask-Assets
    LOAD_PATH = basedir
    # LESS_BIN = path.join(basedir, 'node_modules\\.bin\\lessc')
    ASSETS_DEBUG = False
    ASSETS_AUTO_BUILD = True

    # Static Assets
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'

    # Database
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False

    # Flask-Session
    SESSION_TYPE = 'redis'
    SESSION_REDIS = redis.from_url(environ.get('SESSION_REDIS'))


class DevConfig(Config):

    # Flask
    FLASK_ENV = 'development'
    TESTING = True
    DEBUG = True

    # Database
    SQLALCHEMY_DATABASE_URI = environ.get('DEV_DATABASE_URI')


class ProdConfig(Config):

    # Flask
    FLASK_ENV = 'production'
    TESTING = False
    DEBUG = False

    # Database
    SQLALCHEMY_DATABASE_URI = environ.get('PROD_DATABASE_URI')
