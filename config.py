import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))

#######################################
# Flask-SQLAlchemy
#######################################
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'test.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')


#######################################
# Flask-Security
#######################################
CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'


###########################################################################
# basedir = os.path.abspath(os.path.dirname(__file__))
# app_dir = os.path.abspath(os.path.dirname(__file__))


# class BaseConfig:
#     SECRET_KEY = os.environ.get('SECRET_KEY') or 'A SECRET KEY'
#     SQLALCHEMY_TRACK_MODIFICATIONS = False

#     # настройка Flask-Mail
#     MAIL_SERVER = 'smtp.googlemail.com'
#     MAIL_PORT = 587
#     MAIL_USE_TLS = True
#     MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or 'YOU_MAIL@gmail.com'
#     MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or 'password'
#     MAIL_DEFAULT_SENDER = MAIL_USERNAME


# class DevelopementConfig(BaseConfig):
#     DEBUG = True
#     SQLALCHEMY_DATABASE_URI = os.environ.get('DEVELOPMENT_DATABASE_URI') or \
#         'sqlite:///' + os.path.join(basedir, 'test.db')


# class TestingConfig(BaseConfig):
#     DEBUG = True
#     SQLALCHEMY_DATABASE_URI = os.environ.get('TESTING_DATABASE_URI') or \
#         'sqlite:///' + os.path.join(basedir, 'test.db')


# class ProductionConfig(BaseConfig):
#     DEBUG = False
#     SQLALCHEMY_DATABASE_URI = os.environ.get('PRODUCTION_DATABASE_URI') or \
#         'sqlite:///' + os.path.join(basedir, 'test.db')
