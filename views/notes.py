from flask import flash, render_template, request, redirect, url_for
from flask_login import login_required, current_user

from config import app, db
from models import File, Note
from utils.files_utils import add_at_note_and_save_files


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
            note = add_at_note_and_save_files(
                request.files.getlist('files'), note
            )
            db.session.add(note)
            db.session.commit()
        except Exception as e:
            flash(f'При добавлении заметки произошла ошибка: {e}', 'danger')
            return redirect(request.url)
        flash('Заметка добавлена', 'success')
        return redirect(url_for('note', id=note.id))
    else:
        endpoint = request.endpoint
        return render_template('create_note.html', endpoint=endpoint)


@app.route('/notes/<int:id>')
def note(id):
    note = Note.get_by_id(id)
    if not note:
        return redirect(url_for('notes'))
    if not note:
        flash('Заметка не найдена', 'danger')
        return redirect(url_for('notes'))
    return render_template('note.html', note=note)


@app.route('/notes/<int:id>/delete')
@login_required
def delete_note(id):
    note = Note.query.get_or_404(id)
    try:
        db.session.delete(note)
        db.session.commit()
        flash('Заметка удалена', 'success')
        return redirect('/notes', code=302)
    except Exception:
        flash('При удалении заметки произошла ошибка', 'danger')
        return redirect(url_for('notes'), code=302)

@app.route('/notes/<int:id>/confirmation')
@login_required
def confirmation(id):
    note = Note.get_by_id(id)
    if not note:
        flash('Заметка не найдена', 'danger')
        return redirect(url_for('notes'))
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
        return redirect(url_for('note', id=note.id), code=302)
    except Exception:
        flash('При добавлении заметки в избранное произошла ошибка', 'danger')
        return redirect(url_for('notes'), code=302)


@app.route('/notes/<int:id>/unfavorite')
@login_required
def unfavorite(id):
    note = Note.get_by_id(id)
    user = current_user
    if not note or not user:
        flash('Заметка или пользователь не найдены', 'danger')
        return redirect(url_for('notes'))
    if note not in user.favorite_notes:
        flash('Заметка уже не в избранном', 'danger')
        return redirect(url_for('note', id=note.id), code=302)
    user.favorite_notes.remove(note)
    try:
        db.session.commit()
        if user.is_author(note):
            flash('Заметка удалена из избранного', 'success')
            return redirect(url_for('note', id=note.id), code=302)
        else:
            flash('Заметка удалена из избранного', 'success')
            return redirect(url_for('note', id=note.id), code=302)
    except Exception:
        flash('При удалении заметки из избранного произошла ошибка', 'danger')
        return redirect(url_for('notes'), code=302)


@app.route('/notes/<int:note_id>/edit', methods=['POST', 'GET'])
@login_required
def edit_note(note_id):
    note = Note.get_by_id(note_id)
    if not current_user.is_author(note):
        flash('Вы не можете редактировать чужую заметку', 'danger')
        return redirect(url_for('notes'))
    endpoint = request.endpoint
    if request.method == 'POST':
        note.title = request.form.get('title')
        note.intro = request.form.get('intro')
        note.text = request.form.get('text')
        note.public = request.form.get('public')
        note = add_at_note_and_save_files(request.files.getlist('files'), note)
        try:
            db.session.commit()
            flash('Заметка обновлена', 'success')
            return redirect(url_for('notes'), code=302)
        except Exception as e:
            flash(f'При обновлении заметки произошла ошибка {e}', 'danger')
            return redirect(url_for('note', id=note.id), code=302)
    if not note:
        flash('Заметка не найдена', 'danger')
        return redirect(url_for('notes'))
    files = File.query.filter(File.notes.contains(note)).all()
    return render_template(
        'create_note.html', note=note, endpoint=endpoint, files=files
    )


@app.route('/notes/favorites')
@login_required
def favorites():
    endpoint = request.endpoint
    if current_user.is_authenticated:
        user = current_user
        notes = (Note.query.filter(Note.favorites.contains(user))
                           .order_by(Note.id.desc())
                           .all())
        return render_template('notes.html', notes=notes, endpoint=endpoint)
    else:
        return render_template('notes.html', endpoint=endpoint)


@app.route('/remove_files/<int:note_id>')
def remove_files(note_id):
    note = Note.get_by_id(note_id)
    if not current_user.is_author(note):
        flash('Вы не можете удалять файлы из чужой заметки', 'danger')
        return redirect(url_for('note', id=note_id))
    if not note:
        flash('Заметка не найдена', 'danger')
        return redirect(url_for('notes'))
    note.files = []  # дописать очистку памяти хранилища
    try:
        db.session.commit()
        return redirect(url_for('edit_note', note_id=note_id), code=302)
    except Exception as e:
        flash(f'При удалении файла из заметки произошла ошибка {e}', 'danger')
        return redirect(url_for('note', id=note_id), code=302)


@app.route('/notes/public')
def public():
    endpoint = request.endpoint
    notes = Note.query.filter_by(public='on').order_by(Note.id.desc()).all()
    return render_template('notes.html', notes=notes, endpoint=endpoint)
