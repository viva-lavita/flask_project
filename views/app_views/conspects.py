import os
from flask import flash, render_template, request, redirect, url_for
from flask_login import login_required, current_user

from utils.decorators import roles_required

from .app import app, db
from models import (
    Conspect, Message, conspect_file, favorites, File, Note, note_file, User
)
from utils.files_utils import (
    add_at_conspects_and_save_files, add_at_conspect_and_save_images,
    check_file_exsists, check_md_file, get_md
)


@app.route('/conspects/<int:id>')
def conspect(id):
    conspect = Conspect.get_by_id(id)
    if not conspect:
        flash('Конспект не найден', 'danger')
        return redirect(url_for('app.conspects'))

    html_text = get_md(conspect.name)
    name = conspect.name.rsplit('.', 1)[0]
    return render_template('conspect.html',
                           markdown=html_text,
                           item=conspect,
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
    if current_user.is_authenticated:
        conspects = (Conspect.query
                             .filter(Conspect.user_id == current_user.id)
                             .order_by(Conspect.id.desc())
                             .all())
        return render_template('conspects.html',
                               conspects=conspects)
    return render_template('conspects.html')


@app.route('/conspects/<int:id>/add_intro', methods=['GET', 'POST'])
@login_required
def add_intro(id):
    """ Добавление описания, метки public и иллюстраций. """
    conspect = Conspect.get_by_id(id)
    if not current_user.is_author(conspect):
        flash('У вас нет прав на редактирование этого конспекта', 'danger')
        return redirect(url_for('app.conspect', id=id))
    if request.method == 'POST':
        conspect.intro = request.form['intro']
        conspect.public = request.form.get('public')
        images = request.files.getlist('images')
        add_at_conspect_and_save_images(images, id)
        db.session.commit()
        return redirect(url_for('app.conspect', id=id))
    return render_template('add_intro.html', conspect=conspect)


@app.route('/conspects/<int:id>/confirm')
@login_required
def confirmation_conspect(id):
    """ Эндпоинт подтверждения удаления. """
    conspect = Conspect.get_by_id(id)
    if not conspect:
        flash(f'Конспект c id-{id} не найден', 'danger')
        return redirect(url_for('app.conspects'))
    if not current_user.is_author(conspect):
        flash('У вас нет прав на удаление этого конспекта', 'danger')
        return redirect(url_for('app.conspect', id=id))
    return render_template('confirmation.html', conspect=conspect)


@app.route('/conspects/<int:id>/delete')
@login_required
def delete_conspect(id):
    """ Удаление конспекта. """
    conspect = Conspect.get_by_id(id)
    if not current_user.is_author(conspect):
        flash('У вас нет прав на удаление этого конспекта', 'danger')
        return redirect(url_for('app.conspect', id=id))
    if not conspect:
        flash(f'Конспект c id-{id} не найден', 'danger')
        return redirect(url_for('app.conspects'))
    name = conspect.name
    file = File.query.filter(File.name == name).first()
    try:
        db.session.delete(conspect)
        db.session.commit()
        flash('Конспект удален', 'success')
        if not File.is_used_in_conspect(file):
            os.remove(os.path.join(app.config.get('UPLOAD_FOLDER'), name))
            flash('окончательно, ни единого экземпляра на сервере не осталось',
                  'success')
    except Exception as e:
        flash(f'При удалении конспекта произошла ошибка: {e}', 'danger')
        return redirect(url_for('app.conspects'))
    return redirect(url_for('app.conspects'))


@app.route('/delete_all')   # эндпоинт самоуничтожения. Для отладки!
@login_required
@roles_required("admin")
def delete_all():
    db.session.query(favorites).delete()
    db.session.query(note_file).delete()
    db.session.query(conspect_file).delete()
    db.session.query(File).delete()
    db.session.query(Note).delete()
    db.session.query(Conspect).delete()
    db.session.query(Message).delete()
    db.session.commit()

    folder_path = os.path.join(app.static_folder, 'media', 'uploads')
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        os.remove(file_path)
    return redirect(url_for('app.upload_conspects'))


@app.route('/conspects/<int:id>/favorite')
@login_required
def favorite_conspect(id):
    """ Добавление конспекта в избранное. """
    conspect = Conspect.get_by_id(id)
    if not conspect:
        return f'Конспект {id} не найден'
    current_user.favorite_conspects.append(conspect)
    try:
        db.session.commit()
        flash('Конспект добавлен в избранное', 'success')
        return redirect(url_for('app.conspect', id=id), code=302)
    except Exception as e:
        flash(f'При добавлении конспекта в избранное произошла ошибка {e}',
              'danger')
        return redirect(url_for('app.conspect', id=id), code=302)


@app.route('/conspects/<int:id>/unfavorite')
@login_required
def unfavorite_conspect(id):
    """ Удаление конспекта из избранного. """
    conspect = Conspect.get_by_id(id)
    if not conspect:
        return f'Конспект {id} не найден'
    current_user.favorite_conspects.remove(conspect)
    try:
        db.session.commit()
        flash('Конспект удален из избранного', 'success')
        return redirect(url_for('app.conspect', id=id), code=302)
    except Exception as e:
        flash(f'При удалении конспекта из избранного произошла ошибка {e}',
              'danger')
        return redirect(url_for('app.conspects'), code=302)


@app.route('/conspects/favorites')
@login_required
def favorite_conspects():
    """ Список всех добавленных в избранное конспектов. """
    conspects = (
        Conspect.query.filter(Conspect.favorites.contains(current_user))
                      .order_by(Conspect.id.desc())
                      .all()
    )
    return render_template('conspects.html', conspects=conspects)


@app.route('/conspects/public')
def public_conspects():
    """ Список конспектов в публичном доступе. """
    conspects = Conspect.get_public_conspects()
    return render_template('conspects.html', conspects=conspects)


@app.route('/conspects/<int:conspect_id>/remove_images')
def remove_images(conspect_id):
    """ Эндпоинт для кнопки удаления картинок из конспекта. """
    conspect = Conspect.get_by_id(conspect_id)
    if not current_user.is_author(conspect):
        flash('Вы не можете удалять фотографии из чужого конспекта', 'danger')
        return redirect(url_for('app.conspect', id=conspect_id))
    if not conspect:
        flash(f'Конспект c id-{conspect_id} не найден', 'danger')
        return redirect(url_for('app.conspects'))
    files = File.query.filter(File.img_conspects.contains(conspect)).all()
    try:
        for file in files:
            if check_md_file(file.name):
                continue
            if check_file_exsists(file.name):
                conspect.images.remove(file)
                os.remove(
                    os.path.join(app.config.get('UPLOAD_FOLDER'),
                                 file.name)
                )
        db.session.commit()
        return redirect(url_for('app.add_intro', id=conspect_id), code=302)
    except Exception as e:
        flash(f'При удалении файла из заметки произошла ошибка {e}',
              'danger')
        return redirect(url_for('app.conspect', id=conspect_id), code=302)


@app.route('/user_<int:user_id>/conspects')
def user_conspects(user_id):
    if user_id == current_user.id:
        return redirect(url_for('app.conspects'))
    user = User.get_by_id(user_id)
    if current_user.is_authenticated:
        conspects = (Conspect.query
                             .filter(Conspect.user_id == user.id)
                             .order_by(Conspect.id.desc())
                             .all())
        return render_template('conspects.html',
                               conspects=conspects,
                               user=user)
    return render_template('conspects.html')


@app.route('/follow_conspects')
@login_required
def follow_conspects():
    follows_id = [author.id for author in current_user.followed_list()]
    conspects = Conspect.query.filter(Conspect.user_id.in_(follows_id)).all()
    return render_template('conspects.html', conspects=conspects)
