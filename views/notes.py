from flask import render_template, request, redirect
from flask_login import login_required, current_user

from config import app, db
from models import Note


@app.route('/notes')
def notes():
    endpoint = request.endpoint
    if current_user.is_authenticated:
        user = current_user
        notes = (Note.query
                     .filter(Note.user_id == user.id)
                     .order_by(Note.data.desc())
                     .all())
        return render_template('notes.html', notes=notes, endpoint=endpoint)
    else:
        return render_template('notes.html', endpoint=endpoint)


@app.route('/create_note', methods=['GET', 'POST'])
@login_required
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
@login_required
def note(id):
    note = Note.get_by_id(id)
    if not note:
        return 'Заметка не найдена'
    return render_template('note.html', note=note)


@app.route('/notes/<int:id>/delete')
@login_required
def delete_note(id):
    note = Note.query.get_or_404(id)
    try:
        db.session.delete(note)
        db.session.commit()
        return redirect('/notes', code=302)
    except Exception:
        return 'При удалении заметки произошла ошибка'


@app.route('/notes/<int:id>/confirmation')
@login_required
def confirmation(id):
    note = Note.get_by_id(id)
    if not note:
        return 'Заметка не найдена'
    return render_template('confirmation.html', note=note)


@app.route('/notes/<int:id>/favorite')
@login_required
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
@login_required
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
@login_required
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


@app.route('/notes/favorites')
@login_required
def favorites():
    endpoint = request.endpoint
    if current_user.is_authenticated:
        user = current_user
        notes = (Note.query.filter(Note.favorites.contains(user))).all()
        return render_template('notes.html', notes=notes, endpoint=endpoint)
    else:
        return render_template('notes.html', endpoint=endpoint)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
