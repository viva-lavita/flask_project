import random
import string
import logging

from flask import flash, render_template, request, redirect, url_for
from flask_login import login_required, login_user, logout_user, current_user
from config import mail, Message

from .app import app, db
from models import User


logger = logging.getLogger('my_logger')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if not username or not password:
            flash('Все поля должны быть заполнены', 'danger')
            return redirect(url_for('login'))
        user = db.session.query(User).filter(User.username == username).first()
        if user and user.check_password(password):
            login_user(user, remember=True)
            # flash('Вы вошли в систему', 'success')

            # try:
            #     a = 2/0
            #     raise ValueError('Something went wrong')
            # except ValueError as e:
            #     logger.error(str(e))             # !!!!!дотестить логирование
            # return redirect(url_for('notes'))
        else:
            flash('Неправильное имя пользователя или пароль', 'danger')
            return render_template('login.html')
    if current_user.is_authenticated:
        flash('Добро пожаловать! Вам тут всегда рады =)', 'success')
        return redirect(url_for('notes'))
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы вышли из аккаунта. Ждем Вас вновь!', 'success')
    return render_template('index.html')


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        if not username or not password or not email:
            flash('Все поля должны быть заполнены', 'danger')
            return redirect(url_for('register'))
        if User.query.filter(User.username == username).first():
            flash('Пользователь с таким именем уже существует', 'danger')
            return redirect(url_for('register'))
        user = User(username=username, email=email)
        user.set_password(password)
        try:
            db.session.add(user)
            db.session.commit()
            # flash('Пользователь успешно добавлен', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            print(e)
            flash('При добавлении пользователя произошла ошибка', 'danger')
            return redirect(url_for('login'))
    if current_user.is_authenticated:
        return redirect(url_for('notes'))
    return render_template('login.html')


@app.route('/restoring_access', methods=['POST', 'GET'])
def restoring_access():  # Явно нужно переписать + убрать текст
    if current_user.is_authenticated:
        return redirect(url_for('notes'))
    if request.method == 'POST':
        email = request.form.get('email')
        user = User.query.filter(User.email == email).first()
        if not user:
            flash('Пользователь с таким email не найден', 'danger')
            return redirect(url_for('restoring_access'))
        new_password = ''.join(random.choices(string.ascii_letters +
                                              string.digits, k=12))
        try:
            user.set_password(new_password)
            db.session.commit()
        except Exception:
            flash('При обновлении пароля произошла ошибка', 'danger')
            return redirect(url_for('restoring_access'))

        msg = Message('Восстановление доступа', recipients=[email])
        msg.html = f'''
        <h1>Восстановление доступа к аккаунту NoteVi</h1>
        <p>Ваш новый пароль: {new_password}</p>
        <p>Ваш логин: {user.username}</p>
        '''
        try:
            mail.send(msg)
        except Exception:
            flash('При отправке письма произошла ошибка', 'danger')
            return redirect(url_for('restoring_access'))
        flash('Новый пароль отправлен на почту', 'success')
        return redirect(url_for('login'))
    return render_template('login.html')
