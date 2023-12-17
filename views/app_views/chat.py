import ast
import json
from flask import request, render_template, redirect, url_for, session, flash
from flask_login import login_required, current_user

from utils.generate_room_code import generate_room_code
from views import app
from models import User, Chat, Message


# rooms = {}


# @app.route('/chat', methods=["GET", "POST"])
# def home():
#     session.clear()

#     if request.method == "POST":
#         name = request.form.get('name')
#         create = request.form.get('create', False)
#         code = request.form.get('code')
#         join = request.form.get('join', False)

#         if not name:
#             return render_template(
#                 'home.html', error="Name is required", code=code
#             )

#         if create is not False:
#             room_code = generate_room_code(6, list(rooms.keys()))
#             new_room = {
#                 'members': 0,
#                 'messages': []
#             }
#             rooms[room_code] = new_room

#         if join is not False:
#             # no code
#             if not code:
#                 return render_template(
#                     'home.html',
#                     error="Please enter a room code to enter a chat room",
#                     name=name
#                 )
#             # invalid code
#             if code not in rooms:
#                 return render_template(
#                     'home.html',
#                     error="Room code invalid",
#                     name=name
#                 )

#             room_code = code

#         session['room'] = room_code
#         session['name'] = name
#         return redirect(url_for('app.room'))
#     else:
#         return render_template('home.html')


# @app.route('/room')
# def room():
#     room = session.get('room')
#     name = session.get('name')

#     if name is None or room is None or room not in rooms:
#         return redirect(url_for('app.home'))

#     messages = rooms[room]['messages']
#     return render_template(
#         'room.html', room=room, user=name, messages=messages
#     )


# @app.route("chat/<int:chat_id>")
# def chat2(chat_id):
#     print('ID чата', chat_id)
#     if not current_user.is_authenticated:
#         return redirect(url_for("app.login"))
#     chat = Chat.get_by_id(chat_id)
#     if not chat:
#         flash("Чат не найден", "error")
#         return redirect(url_for("app.index"))
#     user_id = session.get('user_id')
#     user = User.get_by_id(user_id)
#     print('Пользователь', user)
#     if not user:
#         flash("Пользователь не найден", "error")
#         return redirect(url_for("app.index"))
#     if user.id != chat.user_id and user.id != chat.recipient_id:
#         flash("Чат не найден", "error")
#         return redirect(url_for("app.index"))
#     chat_data = session.get('chat_data')
#     messages = chat.get_last_100_messages()
#     return render_template("chat2.html",
#                            current_chat=chat,
#                            user=user,
#                            chat_data=chat_data,
#                            messages=messages)


@app.route("<int:user_id>/chat>")
def chat(user_id):
    if not current_user.is_authenticated:
        return redirect(url_for("app.login"))
    user = User.get_by_id(user_id)
    chats = current_user.get_all_chats()
    current_chat = [chat for chat in chats if
                    chat.recipient_id == user.id and
                    chat.user_id == current_user.id or
                    chat.user_id == user.id and
                    chat.recipient_id == current_user.id]
    if len(current_chat) > 0:
        current_chat = current_chat[0]
    else:
        current_chat = current_user.create_chat(user_id)
    chat_data = {}
    if chats:
        for chat in chats:
            if chat.id != current_chat.id:
                if chat.recipient_id != current_user.id:
                    user_chat = User.get_by_id(chat.recipient_id)
                    chat_data[chat.id] = user_chat
                else:
                    user_chat = User.get_by_id(chat.user_id)
                    chat_data[chat.id] = user_chat
    session.clear()
    # session['user_id'] = user_id
    session['chat_id'] = current_chat.id
    session['current_user_id'] = current_user.id
    session['current_username'] = current_user.username
    messages = chat.get_last_100_messages()
    return render_template("chat2.html",
                           current_chat=chat,
                           user=user,
                           chat_data=chat_data,
                           messages=messages)
