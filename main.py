from datetime import datetime
import html
import json
import sys
import logging
from logging.handlers import SMTPHandler

from dotenv import load_dotenv
from flask import Flask, redirect, request, url_for, session
from flask_mail import Mail, Message
from flask_migrate import Migrate
from flask_login import current_user
from flask_socketio import SocketIO, emit, send, join_room, leave_room
from flask_wtf import CSRFProtect

sys.path.append('new_config')
from models import User, Group, Role, Chat, Message as MessageModel
from views import app
from flask_socketio import SocketIO, join_room, leave_room, send

from models import db, login_manager


load_dotenv()

app_main = Flask(__name__)

app_main.config.from_object('new_config.DevelopementConfig')

db.init_app(app_main)

migrate = Migrate()
migrate.init_app(app_main, db)

csrf = CSRFProtect()
csrf.init_app(app_main)

login_manager.init_app(app_main)
login_manager.login_view = 'app.login'
login_manager.login_message = "Авторизуйтесь для доступа к закрытым страницам"
login_manager.login_message_category = "success"

mail = Mail()
mail.init_app(app_main)

# cache = Cache()  # только на проде
# cache.init_app(app_main)

socketio = SocketIO(app_main, async_mode='threading', cors_allowed_origins='*')


@app_main.template_filter('custom_date')
def custom_date(timestamp):
    """ Фильтр для даты в чате """
    current_date = datetime.now().date()
    message_date = timestamp.date()

    if message_date == current_date:
        return timestamp.strftime('%H:%M:%S')
    else:
        return timestamp.strftime('%Y.%m.%d %H:%M:%S')


def ack():  # может дописать доставленное сообщение, галочки там..?
    print('message was received!')


@socketio.on('message')
def handle_message(data):
    chat_id = data.get('chat_id')
    if not chat_id:
        return
    socketio.emit('message', data, to=chat_id, include_self=True)


# @socketio.on('connect')
# def handle_connect():
#     user_id = current_user.id
#     chat_id = session.get('chat_id')
#     username = current_user.username
#     try:
#         data = {
#             "sender_id": user_id,
#             "body": "Пользователь {0} в чате".format(username),
#             "timestamp": str(datetime.now().strftime('%Y.%m.%d %H:%M:%S')),
#         }
#         data = json.dumps(data)
#         join_room(chat_id)
#         send(data, room=chat_id)
#     except Exception as e:
#         print(e)


@socketio.on('join_chat')
def handle_join_room(chat_id):
    user_id = current_user.id
    chat_id = int(chat_id)
    username = current_user.username
    try:
        data = {
            "sender_id": user_id,
            "body": "Пользователь {0} в чате".format(username),
            "timestamp": str(datetime.now().strftime('%Y.%m.%d %H:%M:%S')),
        }
        data = json.dumps(data)
        join_room(chat_id)
        send(data, room=chat_id)
    except Exception as e:
        print(e)


@socketio.on('leave_chat')
def handle_leave_room(chat_id):
    user_id = current_user.id
    chat_id = int(chat_id)
    username = current_user.username
    try:
        data = {
            "sender_id": user_id,
            "body": "Пользователь {0} вышел из чата".format(username),
            "timestamp": str(datetime.now().strftime('%Y.%m.%d %H:%M:%S')),
        }
        data = json.dumps(data)
        leave_room(chat_id)
        send(data, to=chat_id)
    except Exception as e:
        print(e)


@socketio.on('disconnect')
def handle_disconnect():
    chat_id = session.get('chat_id')
    if chat_id is None:
        return print('Пользователь вышел из чата', session.get('chat_id'))
    chat_id = int(chat_id)
    session['chat_id'] = 0
    handle_leave_room(chat_id)


@socketio.on('new_message')
def handle_new_message(data: dict):
    try:
        chat_id = session.get('chat_id')
        sender_id = data["sender_id"]
        recipient_id = data["recipient_id"]
        body = data["body"]

        message = MessageModel(chat_id=chat_id,
                               sender_id=sender_id,
                               recipient_id=recipient_id,
                               body=body)

        current_chat = db.session.get(Chat, chat_id)
        current_chat.messages.append(message)
        message.save()
        data = json.dumps(message.__json__())
        emit("new_message", data, to=chat_id, callback=ack())
    except Exception as e:
        print(e)


# Хранит идентификаторы пользователей и время их последнего онлайного статуса
TAG_ONLINE_STORAGE = {}


def filling_online_storage():
    """Заполняет хранилище онлайн статусов."""
    if TAG_ONLINE_STORAGE:
        return
    for user in User.query.all():
        TAG_ONLINE_STORAGE[user.id] = ''


@socketio.on('online')
def handle_online(data):
    TAG_ONLINE_STORAGE[current_user.id] = data['timestamp']


@socketio.on('check_timestamp')
def handle_chack_online(users_ids) -> None:
    users_ids = json.loads(html.unescape(users_ids))
    new_users_ids = {}
    for user_id in users_ids:
        new_users_ids[int(user_id)] = TAG_ONLINE_STORAGE.get(int(user_id), '')
    sender_sid = request.sid
    current_time = datetime.now().strftime('%Y.%m.%d %H:%M:%S')
    data_to_emit = {
        'new_users_ids': new_users_ids,
        'current_time': current_time
    }
    socketio.emit('render_online_tags',
                  data_to_emit,
                  to=sender_sid)


if not app_main.debug:

    mail_handler = SMTPHandler(
        mailhost=(app_main.config['MAIL_SERVER'], app_main.config['MAIL_PORT']),
        fromaddr=app_main.config['SECURITY_EMAIL_SENDER'],
        toaddrs=app_main.config['MAIL_USERNAME'],
        subject='Error occurred!',
        credentials=(app_main.config['MAIL_USERNAME'], app_main.config['MAIL_PASSWORD']),
        secure=()
    )
    mail_handler.setLevel(logging.ERROR)
    logger = logging.getLogger()
    logger.addHandler(mail_handler)

# Настройка файла логирования !!!!!!!!!!добавить ограничение размера!!!!!!!!!
file_handler = logging.FileHandler('app.log')
file_handler.setLevel(logging.ERROR)

# Создание форматтера для указания формата записи логов
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
file_handler.setFormatter(formatter)

# Получение корневого логгера
logger = logging.getLogger()
logger.addHandler(file_handler)


def create_admin():
    if db.session.query(User).filter(User.username == 'admin').first():
        return
    role = Role(name='admin')
    group = Group(name='administrators')
    group.roles.append(role)
    password = '1478951'
    user = User(
        username='admin',
        email='pCwfK7@example.com',
        name='админ',
        surname='админ',
        profession='Full Stack Developer',
        city='Moscow',
        phone='+7-999-999-99-99',
        birth_date=datetime(1990, 1, 1)
    )
    user.set_password(password)
    user.groups.append(group)
    db.session.add(user)
    db.session.commit()
    print('Админ создан')


if __name__ == '__main__':
    with app_main.app_context():
        try:
            app_main.register_blueprint(app)
            # app_main.register_blueprint(socketio)
            db.create_all()
            create_admin()
            filling_online_storage()
            sys.stdout.write('База данных обновлена')
        except Exception as e:
            sys.stdout.write(f'Ошибка создания БД: + {e}')
    socketio.run(app_main, host='0.0.0.0', port=5000, debug=True)
