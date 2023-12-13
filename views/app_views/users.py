import random
import string
import logging

from flask import flash, render_template, request, redirect, url_for
from flask_login import login_required, login_user, logout_user, current_user
from new_main import mail, Message

from .app import app, db
from models import Conspect, Note, User
from utils.progress import progress
from forms.edit_profile_form import EditProfileForm


logger = logging.getLogger('my_logger')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if not username or not password:
            flash('Все поля должны быть заполнены', 'danger')
            return redirect(url_for('app.login'))
        user = db.session.query(User).filter(User.username == username).first()
        if user and user.check_password(password):
            login_user(user, remember=True)
            # flash('Вы вошли в систему', 'success')

            # try:
            #     a = 2/0
            #     raise ValueError('Something went wrong')
            # except ValueError as e:
            #     logger.error(str(e))             # !!!!!дотестить логирование
            # return redirect(url_for('app.notes'))
        else:
            flash('Неправильное имя пользователя или пароль', 'danger')
            return render_template('login.html')
    if current_user.is_authenticated:
        flash('Добро пожаловать! Вам тут всегда рады =)', 'success')
        return redirect(url_for('app.notes'))
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
            return redirect(url_for('app.register'))
        if User.query.filter(User.username == username).first():
            flash('Пользователь с таким именем уже существует', 'danger')
            return redirect(url_for('app.register'))
        user = User(username=username, email=email)
        user.set_password(password)
        try:
            db.session.add(user)
            db.session.commit()
            # flash('Пользователь успешно добавлен', 'success')
            return redirect(url_for('app.login'))
        except Exception as e:
            print(e)
            flash('При добавлении пользователя произошла ошибка', 'danger')
            return redirect(url_for('app.login'))
    if current_user.is_authenticated:
        return redirect(url_for('app.notes'))
    return render_template('login.html')


@app.route('/restoring_access', methods=['POST', 'GET'])
def restoring_access():  # Явно нужно переписать + убрать текст
    if current_user.is_authenticated:
        return redirect(url_for('app.notes'))
    if request.method == 'POST':
        email = request.form.get('email')
        user = User.query.filter(User.email == email).first()
        if not user:
            flash('Пользователь с таким email не найден', 'danger')
            return redirect(url_for('app.restoring_access'))
        new_password = ''.join(random.choices(string.ascii_letters +
                                              string.digits, k=12))
        try:
            user.set_password(new_password)
            db.session.commit()
        except Exception:
            flash('При обновлении пароля произошла ошибка', 'danger')
            return redirect(url_for('app.restoring_access'))

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
            return redirect(url_for('app.restoring_access'))
        flash('Новый пароль отправлен на почту', 'success')
        return redirect(url_for('app.login'))
    return render_template('login.html')


@app.route('/<int:user_id>/profile')
@login_required
def profile(user_id):
    user = User.get_by_id(user_id)
    notes = Note.query.filter(Note.user_id == user.id)
    conspects = Conspect.query.filter(Conspect.user_id == user.id)
    progress_bar = progress(user)
    form = EditProfileForm()
    return render_template('profile.html',
                           notes=notes,
                           conspects=conspects,
                           user=user,
                           progress_bar=progress_bar,
                           form=form)


@app.route('/best_authors')
@login_required
def best_authors():
    followed_users = current_user.followed_list()
    progress_bar = progress(current_user)
    return render_template('best_authors.html',
                           progress_bar=progress_bar,
                           follows=followed_users)


@app.route('/<int:user_id>/follow')
@login_required
def follow(user_id):
    user = User.get_by_id(user_id)
    if user is None:
        flash('Пользователь не найден', 'danger')
        return redirect(url_for('app.profile', user_id=user_id))
    if user == current_user:
        flash('Вы не можете подписаться на себя', 'danger')
        return redirect(url_for('app.profile', user_id=user_id))
    if current_user.is_followed(user):
        flash('Вы уже подписаны на этого пользователя', 'danger')
        return redirect(url_for('app.profile', user_id=user_id))
    current_user.followed.append(user)
    db.session.commit()
    return redirect(request.referrer)


@app.route('/<int:user_id>/unfollow')
@login_required
def unfollow(user_id):
    user = User.get_by_id(user_id)
    if user is None:
        flash('Пользователь не найден', 'danger')
        return redirect(url_for('app.index'))
    if user == current_user:
        flash('Вы не можете отписаться от себя', 'danger')
        return redirect(url_for('app.profile', user_id=current_user.id))
    if not current_user.is_followed(user):
        flash('Вы не подписаны на этого пользователя', 'danger')
        return redirect(url_for('app.index'))
    current_user.followed.remove(user)
    db.session.commit()
    return redirect(request.referrer)


@app.route('/edit_profile', methods=['POST', 'GET'])  # для ушустрения можно записывать количество конспектов и заметок в базу в отдельные поля
@login_required
def edit_profile():
    form = EditProfileForm(obj=current_user)
    notes = Note.query.filter(Note.user_id == current_user.id)
    conspects = Conspect.query.filter(Conspect.user_id == current_user.id)
    progress_bar = progress(current_user)
    if request.method == 'POST':
        if form.validate_on_submit():
            for field in form:
                if (field.name != 'csrf_token' and
                    field.data != '' and
                    field.data != None and
                    field.data != getattr(current_user, field.name)):
                    setattr(current_user, field.name, field.data)
            db.session.commit()
            return redirect(url_for('app.profile',
                                    user_id=current_user.id,
                                    form=form,
                                    notes=notes,
                                    conspects=conspects,
                                    progress_bar=progress_bar))
        for key, value in form.errors.items():
            flash([key, *value], 'danger')
        flash('При редактировании профиля произошла ошибка', 'danger')
        return redirect(url_for('app.profile',
                                user_id=current_user.id,
                                form=form,
                                notes=notes,
                                conspects=conspects,
                                progress_bar=progress_bar))
    return render_template(url_for('app.profile',
                                   user_id=current_user.id,
                                   form=form,
                                   notes=notes,
                                   conspects=conspects,
                                   progress_bar=progress_bar))
