import os
from pathlib import Path

from dotenv import load_dotenv

basedir = Path(__file__).resolve().parent.parent

load_dotenv()


class BaseConfig:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

    # настройка Flask-Mail
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or 'YOU_MAIL@gmail.com'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or 'password'
    MAIL_DEFAULT_SENDER = MAIL_USERNAME

    # настройка Flask-Security
    CSRF_ENABLED = True
    SECRET_KEY = os.environ.get('SECRET_KEY') or \
        'you-will-never-guess'
    SECURITY_REGISTERABLE = True

    # настройка Flask-Mail
    MAIL_SERVER = 'smtp.yandex.ru'
    MAIL_PORT = 465
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or 'YOU_MAIL@gmail.com'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or 'password'
    MAIL_DEFAULT_SENDER = MAIL_USERNAME
    SECURITY_EMAIL_SENDER = MAIL_USERNAME
    ADMINS = [MAIL_USERNAME]
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True

    # Upload Files
    UPLOAD_FOLDER = os.path.join(basedir, 'static', 'media', 'uploads/')
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'md'}
    MAX_CONTENT_LENGTH = 16 * 1000 * 1000

    # Flask-Admin
    FLASK_ADMIN_SWATCH = 'cerulean'


class DevelopementConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'test.db')


class TestingConfig(BaseConfig): # добавить в .env TESTING_DATABASE_URI постгрес локал
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TESTING_DATABASE_URI')
    POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD')

    # Flask-Cache
    CACHE_TYPE = os.environ.get('CACHE_TYPE') or 'SimpleCache'
    CACHE_REDIS_HOST = os.environ.get('CACHE_REDIS_HOST') or 'localhost'
    CACHE_REDIS_PORT = os.environ.get('CACHE_REDIS_PORT') or 6379
    CACHE_REDIS_DBCACHE_REDIS_DB = os.environ.get('CACHE_REDIS_DB') or 0
    CACHE_REDIS_URL = os.environ.get('CACHE_REDIS_URL') or None
    CACHE_REDIS_PASSWORD = os.environ.get('CACHE_REDIS_PASSWORD')
    CACHE_DEFAULT_TIMEOUT = os.environ.get('CACHE_DEFAULT_TIMEOUT') or 10


class ProductionConfig(BaseConfig):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')
    POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD')

    # Flask-Cache
    CACHE_TYPE = os.environ.get('CACHE_TYPE') or 'SimpleCache'
    CACHE_REDIS_HOST = os.environ.get('CACHE_REDIS_HOST') or 'localhost'
    CACHE_REDIS_PORT = os.environ.get('CACHE_REDIS_PORT') or 6379
    CACHE_REDIS_DBCACHE_REDIS_DB = os.environ.get('CACHE_REDIS_DB') or 0
    CACHE_REDIS_URL = os.environ.get('CACHE_REDIS_URL') or None
    CACHE_REDIS_PASSWORD = os.environ.get('CACHE_REDIS_PASSWORD')
    CACHE_DEFAULT_TIMEOUT = os.environ.get('CACHE_DEFAULT_TIMEOUT') or 10
