from datetime import datetime
import json
import sys
import logging
from logging.handlers import SMTPHandler

from dotenv import load_dotenv
from flask import Flask, session
from flask_mail import Mail, Message
from flask_migrate import Migrate
from flask_socketio import SocketIO, emit
from flask_wtf import CSRFProtect

sys.path.append('new_config')
from models import User, Group, Role, Chat, Message as MessageModel
from views import app
# from views.app_views.chat import rooms
from flask_socketio import SocketIO, join_room, leave_room, send

from main import db, login_manager


load_dotenv()

app_main = Flask(__name__)

app_main.config.from_object('new_config.DevelopementConfig')

db.init_app(app_main)

migrate = Migrate()
migrate.init_app(app_main, db)

csrf = CSRFProtect()
csrf.init_app(app_main)

login_manager.init_app(app_main)
login_manager.login_view = 'login'
login_manager.login_message = "Авторизуйтесь для доступа к закрытым страницам"
login_manager.login_message_category = "success"

mail = Mail()
mail.init_app(app_main)

# cache = Cache()  # только на проде
# cache.init_app(app_main)

socketio = SocketIO(app_main, async_mode='threading', cors_allowed_origins='*')


# @socketio.on('connect')
# def handle_connect():
#     name = session.get('name')
#     room = session.get('room')

#     if name is None or room is None:
#         return
#     if room not in rooms:
#         leave_room(room)

#     join_room(room)
#     send({
#         "sender": "",
#         "message": f"{name} has entered the chat"
#     }, to=room)
#     rooms[room]["members"] += 1


# @socketio.on('message')
# def handle_message(payload):
#     room = session.get('room')
#     name = session.get('name')

#     if room not in rooms:
#         return

#     message = {
#         "sender": name,
#         "message": payload["message"]
#     }
#     send(message, to=room)
#     rooms[room]["messages"].append(message)


# @socketio.on('disconnect')
# def handle_disconnect():
#     room = session.get("room")
#     name = session.get("name")
#     leave_room(room)

#     if room in rooms:
#         rooms[room]["members"] -= 1
#         if rooms[room]["members"] <= 0:
#             del rooms[room]

#     send({
#         "message": f"{name} has left the chat",
#         "sender": ""
#     }, to=room)


@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('new_message')
def handle_new_message(data):
    try:
        chat_id = data['chat_id']
        sender_id = data['sender_id']
        recipient_id = data['recipient_id']
        body = data['body']

        message = MessageModel(chat_id=chat_id,
                               sender_id=sender_id,
                               recipient_id=recipient_id,
                               body=body)

        current_chat = db.session.get(Chat, chat_id)
        current_chat.messages.append(message)
        try:
            db.session.add(message)
            db.session.commit()
        except Exception as e:
            print(e)
        data = json.dumps(message.__json__())
        emit('new_message', data, broadcast=True)
    except Exception as e:
        print(e)


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


# def run_app_main():
#     with app_main.app_context():
#         try:
#             app_main.register_blueprint(app)
#             db.create_all()
#             create_admin()
#             sys.stdout.write('База данных обновлена')
#         except Exception as e:
#             sys.stdout.write(f'Ошибка создания БД: {e}')
#     app_main.run(host='0.0.0.0', port=5000)


if __name__ == '__main__':
    with app_main.app_context():
        try:
            app_main.register_blueprint(app)
            # app_main.register_blueprint(socketio)
            db.create_all()
            create_admin()
            sys.stdout.write('База данных обновлена')
        except Exception as e:
            sys.stdout.write(f'Ошибка создания БД: + {e}')
    socketio.run(app_main, host='0.0.0.0', port=5000, debug=True)
