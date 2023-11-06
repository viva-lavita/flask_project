from flask import flash, render_template, request, redirect, url_for
from flask_login import login_required, login_user, logout_user, current_user

from config import app, db
from models import Note, User


@app.route('/admin/')
@login_required
def admin():
    return render_template('admin.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    endpoint = request.endpoint
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = db.session.query(User).filter(User.username == username).first()
        if user and user.check_password(password):
            login_user(user, remember=True)
            flash('Вы вошли в систему', 'success')
            return redirect(url_for('notes'))
        else:
            flash('Неправильное имя пользователя или пароль', 'danger')
            return render_template('login.html', endpoint=endpoint)
    return render_template('login.html', endpoint=endpoint)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return render_template('logout.html')


@app.route('/register', methods=['POST', 'GET'])
def register():
    endpoint = request.endpoint
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        if User.query.filter(User.username == username).first():
            flash('Пользователь с таким именем уже существует', 'danger')
            return redirect(url_for('login'))
        user = User(username=username, email=email)
        user.set_password(password)
        try:
            db.session.add(user)
            db.session.commit()
            flash('Пользователь успешно добавлен', 'success')
            return redirect(url_for('login'))
        except Exception:
            flash('При добавлении пользователя произошла ошибка', 'danger')
            return redirect(url_for('login'))
    return render_template('login.html', endpoint=endpoint)


@app.route('/')
@app.route('/index')
def index():
    endpoint = request.endpoint
    return render_template('index.html', endpoint=endpoint)


@app.route('/about')
def about():
    endpoint = request.endpoint
    return render_template('about.html', endpoint=endpoint)


@app.route('/contact/<string:name>')
def contact(name):
    endpoint = request.endpoint
    return render_template('contact.html', name=name, endpoint=endpoint)


@app.route('/notes')
def notes():
    endpoint = request.endpoint
    notes = Note.query.order_by(Note.data.desc()).all()
    return render_template('notes.html', notes=notes, endpoint=endpoint)


@app.route('/create_note', methods=['GET', 'POST'])
def create_note():
    if request.method == 'POST':
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']
        user = request.args.get('user_id')
        note = Note(title=title, intro=intro, text=text, user_id=user)
        try:
            db.session.add(note)
            db.session.commit()
            return redirect('/notes', code=302)
        except Exception:
            return 'При добавлении заметки произошла ошибка'
    else:
        endpoint = request.endpoint
        return render_template('create_note.html', endpoint=endpoint)


@app.route('/notes/<int:id>')
def note(id):
    note = Note.get_by_id(id)
    if not note:
        return 'Заметка не найдена'
    return render_template('note.html', note=note)


@app.route('/notes/<int:id>/delete')
def delete_note(id):
    note = Note.query.get_or_404(id)
    try:
        db.session.delete(note)
        db.session.commit()
        return redirect('/notes', code=302)
    except Exception:
        return 'При удалении заметки произошла ошибка'


@app.route('/notes/<int:id>/confirmation')
def confirmation(id):
    note = Note.get_by_id(id)
    if not note:
        return 'Заметка не найдена'
    return render_template('confirmation.html', note=note)


@app.route('/notes/<int:id>/favorite')
def favorite(id):
    note = (db.session.query(Note)
            .filter(Note.id == id)
            .first())
    user = current_user
    if not note or not user:
        return f'Заметка или пользователь не найдены {user}'
    user.favorite_notes.append(note)
    try:
        db.session.commit()
        return redirect('/notes/' + str(id), code=302)
    except Exception:
        return 'При добавлении заметки произошла ошибка'


@app.route('/notes/<int:id>/unfavorite')
def unfavorite(id):
    note = (db.session.query(Note)
            .filter(Note.id == id)
            .first())
    user = current_user
    if not note or not user:
        return 'Заметка или пользователь не найдены'
    if note not in user.notes:
        return 'Заметка в избранном пользователя не найдена'
    user.favorite_notes.remove(note)
    try:
        db.session.commit()
        return redirect('/notes/' + str(id), code=302)
    except Exception:
        return 'При удалении заметки произошла ошибка'


@app.route('/notes/<int:id>/edit', methods=['POST', 'GET'])
def edit_note(id):
    endpoint = request.endpoint
    if request.method == 'POST':
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']
        try:
            note = Note.get_by_id(id)
            note.title = title
            note.intro = intro
            note.text = text
            db.session.commit()
            return redirect('/notes/' + str(id), code=302)
        except Exception:
            return 'При обновлении заметки произошла ошибка'
    note = Note.get_by_id(id)
    if not note:
        return 'Заметка не найдена'
    return render_template('create_note.html', note=note, endpoint=endpoint)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
