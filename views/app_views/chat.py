import ast
import json
from flask import request, render_template, redirect, url_for, session, flash
from flask_login import login_required, current_user

from utils.generate_room_code import generate_room_code
from views import app
from models import db, User, Chat, Message


def get_ids_chats_with_unread_messages():
    """
    Функция для получения множества идентификаторов чатов 
    с непрочитанными текущим пользователем сообщениями.
    """
    received_unread_messages = Message.query.filter(
        Message.recipient_id == current_user.id,
        Message.is_read == False,
    )
    chat_id_with_unread_messages = set()
    for message in received_unread_messages:
        chat_id_with_unread_messages.add(message.chat_id)
    return chat_id_with_unread_messages


def make_messages_read(messages):
    """
    Функция для отметки прочитанных сообщений.
    """
    for message in messages:
        message.is_read = True
        db.session.commit()


def get_last_unread_send_messages(chat_id):
    """
    Функция для получения списка непрочитанных отправленных сообщений.
    Для отрисовки галочек непрочитанных отправленных сообщений.
    """
    messages = Message.query.filter(
        Message.chat_id == chat_id,
        Message.is_read == False,
        Message.sender_id == current_user.id,
    )
    return messages


def get_last_unread_receive_messages(chat_id):
    """
    Функция для получения списка непрочитанных полученных сообщений.
    """
    messages = Message.query.filter(
        Message.chat_id == chat_id,
        Message.is_read == False,
        Message.recipient_id == current_user.id,
    )
    return messages

def get_current_chat(chats, user_id):
    """
    Функция для получения текущего чата.
    """
    current_chat_list = [chat for chat in chats if
                         chat.recipient_id == user_id and
                         chat.user_id == current_user.id or
                         chat.user_id == user_id and
                         chat.recipient_id == current_user.id]
    if len(current_chat_list) > 0:
        current_chat = current_chat_list[0]
    else:
        current_chat = current_user.create_chat(user_id)
    return current_chat


@app.route("<int:user_id>/chat")
@login_required
def chat(user_id):
    user = User.get_by_id(user_id)
    chats = current_user.get_all_chats()
    current_chat = get_current_chat(chats, user_id)
    chat_data = {}
    users_ids = {user_id: user_id}
    if chats:
        for chat in chats:
            if chat.id != current_chat.id:
                if chat.recipient_id != current_user.id:
                    recipient_user = User.get_by_id(chat.recipient_id)
                    users_ids[recipient_user.id] = recipient_user.id
                    chat_data[chat.id] = recipient_user
                else:
                    recipient_user = User.get_by_id(chat.user_id)
                    users_ids[recipient_user.id] = recipient_user.id
                    chat_data[chat.id] = recipient_user
    # session.clear()
    session["chat_id"] = current_chat.id
    # session["current_user_id"] = current_user.id
    messages = current_chat.get_last_100_messages()
    users_ids_json = json.dumps(users_ids)
    unread_chats_ids = get_ids_chats_with_unread_messages()
    if current_chat.id in unread_chats_ids:
        unread_chats_ids.discard(current_chat.id)
        make_messages_read(get_last_unread_receive_messages(current_chat.id))
    return render_template("chat2.html",
                           current_chat=current_chat,
                           user=user,
                           chat_data=chat_data,
                           messages=messages,
                           users_ids=users_ids_json,
                           unread_chats_ids=list(unread_chats_ids))


@app.route("/messages_delete")
@login_required
def messages_delete():
    db.session.query(Message).delete()
    db.session.commit()
    return redirect(url_for("app.index"))


@app.route("/chat_list")
@login_required
def chat_list():
    chats = current_user.get_all_chats()
    return render_template("chat_list.html", chats=chats)


@app.route("/check_unread_messages_api/<int:chat_id>")
@login_required
def check_unread_messages_api(chat_id):
    unread_chats_ids = get_ids_chats_with_unread_messages()
    unread_chats_ids.discard(chat_id)
    unread_chats_ids_json = json.dumps(list(unread_chats_ids))
    return unread_chats_ids_json


@app.route("/get_unread_messages_api")
@login_required
def get_unread_messages_api():
    """
    API для получения списка непрочитанных сообщений
    и сопроводительной информации для рендеринга виджета.
    """
    unread_chats_ids = get_ids_chats_with_unread_messages()
    if not unread_chats_ids:
        return ""
    chats = Chat.query.filter(Chat.id.in_(unread_chats_ids))
    data = {'unread_chats_ids': list(unread_chats_ids)}
    for chat in chats:
        sender = User.get_by_id(chat.user_id)
        data[chat.user_id] = {
            'username': sender.username,
            # 'image': sender.avatar  # дописать передачу адреса аватарки
        }
    data_json = json.dumps(data)
    return data_json
