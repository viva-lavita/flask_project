import os
from flask import render_template, request, redirect, url_for
from flask_login import login_required, current_user
# from werkzeug.utils import secure_filename

from config import app, db
from models import Note, File
from utils.files_utils import add_and_save_files


@app.route('/notes')
def notes():
    endpoint = request.endpoint
    if current_user.is_authenticated:
        notes = (Note.query
                     .filter(Note.user_id == current_user.id)
                     .order_by(Note.id.desc())
                     .all())
        return render_template('notes.html', notes=notes, endpoint=endpoint)
    else:
        return render_template('notes.html', endpoint=endpoint)


@app.route('/create_note', methods=['GET', 'POST'])
@login_required
def create_note():
    if request.method == 'POST':
        note = Note(
            title=request.form['title'],
            intro=request.form['intro'],
            text=request.form['text'],
            user_id=current_user.id,
            public=request.form.get('public')
        )
        try:
            note = add_and_save_files(request.files.getlist('files'), note)
            db.session.add(note)
            db.session.commit()
        except Exception as e:
            return f'При добавлении заметки произошла ошибка: {e}'

        return redirect(url_for('note', id=note.id))
    else:
        endpoint = request.endpoint
        return render_template('create_note.html', endpoint=endpoint)


@app.route('/notes/<int:id>')
def note(id):
    note = Note.get_by_id(id)
    if not note:
        return redirect(url_for('notes'))
    files = File.query.filter(File.notes.contains(note)).all()
    if not note:
        return 'Заметка не найдена'
    return render_template('note.html', note=note, files=files)


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
    note = Note.get_by_id(id)
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
    note = Note.get_by_id(id)
    user = current_user
    if not note or not user:
        return 'Заметка или пользователь не найдены'
    if note not in user.favorite_notes:
        return 'Заметка в избранном пользователя не найдена'
    user.favorite_notes.remove(note)
    try:
        db.session.commit()
        if user.is_author(note):
            return redirect('/notes/' + str(id), code=302)
        else:
            return redirect('/notes/public', code=302)
    except Exception:
        return 'При удалении заметки произошла ошибка'


@app.route('/notes/<int:id>/edit', methods=['POST', 'GET'])
@login_required
def edit_note(id):
    note = Note.get_by_id(id)
    endpoint = request.endpoint
    if request.method == 'POST':
        note.title = request.form.get('title')
        note.intro = request.form.get('intro')
        note.text = request.form.get('text')
        note.public = request.form.get('public')
        note.files.clear()
        note = add_and_save_files(request.files.getlist('files'), note)
        try:
            db.session.commit()
            return redirect(url_for('note', id=note.id), code=302)
        except Exception as e:
            return f'При обновлении заметки произошла ошибка {e}'
    if not note:
        return 'Заметка не найдена'
    return render_template('create_note.html', note=note, endpoint=endpoint)


@app.route('/notes/favorites')
@login_required
def favorites():
    endpoint = request.endpoint
    if current_user.is_authenticated:
        user = current_user
        notes = Note.query.filter(Note.favorites.contains(user)).order_by(Note.id.desc()).all()
        return render_template('notes.html', notes=notes, endpoint=endpoint)
    else:
        return render_template('notes.html', endpoint=endpoint)


@app.route('/notes/public')
def public():
    endpoint = request.endpoint
    notes = Note.query.filter_by(public='on').order_by(Note.id.desc()).all()
    return render_template('notes.html', notes=notes, endpoint=endpoint)
