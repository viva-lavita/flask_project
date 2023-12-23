# import os

# from dotenv import load_dotenv
# from flask import Flask
# from flask_caching import Cache
# from flask_mail import Mail, Message
# from flask_migrate import Migrate
# from flask_login import LoginManager
# from flask_sqlalchemy import SQLAlchemy
# from flask_wtf import CSRFProtect


# app = Flask(__name__)

# basedir = os.path.abspath(os.path.dirname(__file__))

# load_dotenv()


# #######################################
# # Flask-SQLAlchemy
# #######################################
# # app.config['SQLALCHEMY_DATABASE_URI'] = (
# #     os.environ.get('DATABASE_URI') or 'sqlite:///' + os.path.join(basedir, 'test.db')
# # )
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)
# migrate = Migrate(app, db)
# app.config['SQLALCHEMY_MIGRATE_REPO'] = os.path.join(basedir, 'db_repository')
# app.config['POSTGRES_PASSWORD'] = os.environ.get('POSTGRES_PASSWORD')


# #######################################
# # Flask-Security
# #######################################
# app.config['CSRF_ENABLED'] = True
# app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or \
#         'you-will-never-guess'
# # allows new registrations to application
# app.config['SECURITY_REGISTERABLE'] = True
# csrf = CSRFProtect(app)


# #######################################
# # Flask-Login
# #######################################
# login_manager = LoginManager(app)
# login_manager.login_view = 'login'
# login_manager.login_message = "Авторизуйтесь для доступа к закрытым страницам"
# login_manager.login_message_category = "success"


# #######################################
# # Flask-Mail
# #######################################
# # to send automatic registration email to user
# # app.config['SECURITY_SEND_REGISTER_EMAIL'] = False
# app.config['MAIL_SERVER'] = 'smtp.yandex.ru'
# app.config['MAIL_PORT'] = 465
# # app.config['MAIL_USE_TLS'] = True
# app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME') or 'YOU_MAIL@gmail.com'
# app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD') or 'password'
# app.config['MAIL_DEFAULT_SENDER'] = app.config['MAIL_USERNAME']
# app.config['SECURITY_EMAIL_SENDER'] = app.config['MAIL_USERNAME']
# app.config['ADMINS'] = [app.config['MAIL_USERNAME']]
# app.config['MAIL_USE_TLS'] = False
# app.config['MAIL_USE_SSL'] = True
# mail = Mail(app)


# ######################################
# # Flask-Cache
# ######################################
# # app.config['CACHE_TYPE'] = os.environ.get('CACHE_TYPE') or 'SimpleCache'
# # app.config['CACHE_REDIS_HOST'] = os.environ.get('CACHE_REDIS_HOST') or 'localhost'
# # app.config['CACHE_REDIS_PORT'] = os.environ.get('CACHE_REDIS_PORT') or 6379
# # app.config['CACHE_REDIS_DB'] = os.environ.get('CACHE_REDIS_DB') or 0
# # app.config['CACHE_REDIS_URL'] = os.environ.get('CACHE_REDIS_URL') or None
# # app.config['CACHE_REDIS_PASSWORD'] = os.environ.get('CACHE_REDIS_PASSWORD')
# # app.config['CACHE_DEFAULT_TIMEOUT'] = os.environ.get('CACHE_DEFAULT_TIMEOUT') or 10
# # cache = Cache(app)


# ######################################
# # Upload Files
# ######################################
# app.config['UPLOAD_FOLDER'] = os.path.join(basedir, 'static', 'media', 'uploads/')
# app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif', 'md'}
# app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000


# ######################################
# # Flask-Admin
# ######################################
# app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'


# ###########################################################################
# # basedir = os.path.abspath(os.path.dirname(__file__))
# # app_dir = os.path.abspath(os.path.dirname(__file__))


# # class BaseConfig:
# #     SECRET_KEY = os.environ.get('SECRET_KEY') or 'A SECRET KEY'
# #     SQLALCHEMY_TRACK_MODIFICATIONS = False

# #     # настройка Flask-Mail
# #     MAIL_SERVER = 'smtp.googlemail.com'
# #     MAIL_PORT = 587
# #     MAIL_USE_TLS = True
# #     MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or 'YOU_MAIL@gmail.com'
# #     MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or 'password'
# #     MAIL_DEFAULT_SENDER = MAIL_USERNAME


# # class DevelopementConfig(BaseConfig):
# #     DEBUG = True
# #     SQLALCHEMY_DATABASE_URI = os.environ.get('DEVELOPMENT_DATABASE_URI') or \
# #         'sqlite:///' + os.path.join(basedir, 'test.db')


# # class TestingConfig(BaseConfig):
# #     DEBUG = True
# #     SQLALCHEMY_DATABASE_URI = os.environ.get('TESTING_DATABASE_URI') or \
# #         'sqlite:///' + os.path.join(basedir, 'test.db')


# # class ProductionConfig(BaseConfig):
# #     DEBUG = False
# #     SQLALCHEMY_DATABASE_URI = os.environ.get('PRODUCTION_DATABASE_URI') or \
# #         'sqlite:///' + os.path.join(basedir, 'test.db')
