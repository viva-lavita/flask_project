import markdown
import os
from flask import flash, render_template, request, redirect, url_for
from flask_login import login_required, current_user

from config import app, db
from models import Conspect, File, note_file, favorites, Note, conspect_file
from utils.files_utils import add_at_conspects_and_save_files


@app.route('/conspects/<int:id>')
def conspect(id):
    conspect = Conspect.get_by_id(id)
    name = conspect.name
    if not name:
        flash('Конспект не найден', 'danger')
        return redirect(url_for('conspects'))

    with open(os.path.join(app.config.get('UPLOAD_FOLDER'),
                           name), 'r', encoding='utf-8') as f:
        markdown_text = f.read()
    html_text = markdown.markdown(markdown_text)
    return render_template('conspect.html',
                           markdown=html_text,
                           conspect=conspect,
                           name=name)


@app.route('/upload_conspects', methods=['GET', 'POST'])
@login_required
def upload_conspects():
    if request.method == 'POST':
        if request.files.getlist('files') == []:
            flash('Файлы отсутствуют', 'danger')
            return redirect(request.url)
        conspect_ids = add_at_conspects_and_save_files(
            request.files.getlist('files'), current_user.id
        )
        if not conspect_ids:
            flash('При добавлении конспектов произошла ошибка', 'danger')
            return redirect(request.url)
        flash(f'Вы добавили {len(conspect_ids)} конспект(а/ов)', 'success')
        return redirect(request.url)
    else:
        return render_template('upload.html')


@app.route('/conspects')
def conspects():
    endpoint = request.endpoint
    if current_user.is_authenticated:
        conspects = (Conspect.query
                             .filter(Conspect.user_id == current_user.id)
                             .order_by(Conspect.id.desc())
                             .all())
        return render_template('conspects.html',
                               endpoint=endpoint,
                               conspects=conspects)
    return render_template('conspects.html', endpoint=endpoint)


@app.route('/conspects/<int:id>/add_intro', methods=['GET', 'POST'])
@login_required
def add_intro(id):
    conspect = Conspect.get_by_id(id)
    if request.method == 'POST':
        conspect.intro = request.form['intro']
        db.session.commit()
        return redirect(url_for('conspect', id=id))
    return render_template('add_intro.html', conspect=conspect)


@app.route('/conspects/<int:id>/confirm')
@login_required
def confirmation_conspect(id):
    conspect = Conspect.get_by_id(id)
    if not conspect:
        flash(f'Конспект c id-{id} не найден', 'danger')
        return redirect(url_for('conspects'))
    if not current_user.is_author(conspect):
        flash('У вас нет прав на удаление этого конспекта', 'danger')
        return redirect(url_for('conspect', id=id))
    return render_template('confirmation.html', conspect=conspect)


@app.route('/conspects/<int:id>/delete')
@login_required
def delete_conspect(id):
    conspect = Conspect.get_by_id(id)
    if not current_user.is_author(conspect):
        flash('У вас нет прав на удаление этого конспекта', 'danger')
        return redirect(url_for('conspect', id=id))
    if not conspect:
        flash(f'Конспект c id-{id} не найден', 'danger')
        return redirect(url_for('conspects'))
    name = conspect.name
    file = File.query.filter(File.name == name).first()
    try:
        db.session.delete(conspect)
        db.session.commit()
        flash('Конспект удален', 'success')
        if not File.is_used_in_conspect(file):
            os.remove(os.path.join(app.config.get('UPLOAD_FOLDER'), name))
            flash('окончательно, ни единого экземпляра на сервере не осталось', 'success')
    except Exception as e:
        flash(f'При удалении конспекта произошла ошибка: {e}', 'danger')
        return redirect(url_for('conspects'))
    return redirect(url_for('conspects'))


@app.route('/delete_all')   # эндпоинт самоуничтожения. Для отладки!
@login_required
def delete_all():
    db.session.query(favorites).delete()
    db.session.query(note_file).delete()
    db.session.query(conspect_file).delete()
    db.session.query(File).delete()
    db.session.query(Note).delete()
    db.session.query(Conspect).delete()
    db.session.commit()

    folder_path = os.path.join(app.static_folder, 'media', 'uploads')
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        os.remove(file_path)
    return redirect(url_for('upload_conspects'))


@app.route('/conspects/<int:id>/favorite')
@login_required
def favorite_conspect(id):
    conspect = Conspect.get_by_id(id)
    if not conspect:
        return f'Конспект {id} не найден'
    current_user.favorite_conspects.append(conspect)
    try:
        db.session.commit()
        flash('Конспект добавлен в избранное', 'success')
        return redirect(url_for('conspects'), code=302)
    except Exception:
        flash('При добавлении конспекта в избранное произошла ошибка', 'danger')
        return redirect(url_for('conspect', id=id), code=302)


@app.route('/conspects/<int:id>/unfavorite')
@login_required
def unfavorite_conspect(id):
    conspect = Conspect.get_by_id(id)
    if not conspect:
        return f'Конспект {id} не найден'
    current_user.favorite_conspects.remove(conspect)
    try:
        db.session.commit()
        flash('Конспект удален из избранного', 'success')
        return redirect(url_for('conspect', id=id), code=302)
    except Exception:
        flash('При удалении конспекта из избранного произошла ошибка', 'danger')
        return redirect(url_for('conspects'), code=302)


@app.route('/conspects/favorites')
@login_required
def favorite_conspects():
    notes = (
        Conspect.query.filter(Conspect.favorites.contains(current_user))
                      .order_by(Conspect.id.desc())
                      .all()
    )
    return render_template('conspects.html', notes=notes)


@app.route('/conspects/public')
def public_conspects():
    conspects = Conspect.get_public_conspects()
    return render_template('public_conspects.html', conspects=conspects)
