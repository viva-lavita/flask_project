from flask import render_template, request, redirect, url_for
from flask_login import login_required

from config import app, db
from models import Note, User


@app.route('/admin/')
@login_required
def admin():
    return render_template('admin.html')


@app.route('/login', methods=['POST',  'GET'])
def login():
    endpoint = request.endpoint
    message = ''
    if request.method == 'POST':
        print(request.form)
    username = request.form.get('username')
    password = request.form.get('password')

    if username == 'root' and password == 'pass':
        message = "Correct username and password"
    else:
        message = "Wrong username or password"

    return render_template('login.html', message=message, endpoint=endpoint)


@app.route('/logout')
def logout(): # дописать!
    endpoint = request.endpoint
    return render_template('logout.html', endpoint=endpoint)

@app.route('/register', methods=['POST',  'GET'])
def register():
    endpoint = request.endpoint
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
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
        try:
            user = request.args.get('user_id')
        except Exception:
            user = 1 # заменить, после добавления функционала авторизации
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
    try:
        note = (db.session.query(Note)
                .join(User)
                .filter(Note.id == id, User.id == request.args.get('user_id'))
                .first())
        user = note.user_id
    except Exception:
        user = 1 # заменить, после добавления функционала авторизации
    if not note or not user:
        return f'Заметка или пользователь не найдены {user}'
    if request.method == 'POST':
        user.notes.append(note)
        try:
            db.session.commit()
            return redirect('/notes/' + str(id), code=302)
        except Exception:
            return 'При добавлении заметки произошла ошибка'


@app.route('/notes/<int:id>/unfavorite')
def unfavorite(id):
    note = Note.get_by_id(id)
    user = User.get_by_id(request.args.get('user_id'))
    if not note or not user:
        return 'Заметка Или пользователь не найдены'
    if request.method == 'DELETE':  # прописать разную кнопку на удаление и добавление
        if note not in user.notes:
            return 'Заметка в избранном пользователя не найдена'
        user.notes.remove(note)
        try:
            db.session.commit()
            return redirect('/notes/' + str(id), code=302)
        except Exception:
            return 'При удалении заметки произошла ошибка'


@app.route('/notes/<int:id>/edit', methods=['POST', 'GET'])
def edit_note(id):
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
    return render_template('edit_note.html', note=note)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
