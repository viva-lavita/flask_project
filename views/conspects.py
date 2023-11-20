import markdown
import os
from flask import flash, render_template, request, redirect, url_for
from flask_login import login_required, current_user

from config import app, db
from models import Conspect, File, note_file, favorites, Note, conspect_file
from utils.files_utils import (
    allowed_file, secure_filename, add_at_conspects_and_save_files
)


@app.route('/conspect/<name>')
def conspect(name):
    with open(os.path.join(app.config.get('UPLOAD_FOLDER'),
                           name), 'r', encoding='utf-8') as f:
        markdown_text = f.read()
    html_text = markdown.markdown(markdown_text)
    return render_template('conspect.html',
                           markdown=html_text,
                           filename=name)


@app.route('/uploads', methods=['GET', 'POST'])
@login_required
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config.get('UPLOAD_FOLDER'), filename))
            return redirect(url_for('index'), code=302)
        else:
            flash('Файл должен иметь формат md')
            return redirect(request.url)
    return render_template('upload.html')


@app.route('/upload_conspects', methods=['GET', 'POST'])
@login_required
def upload_conspects():
    if request.method == 'POST':
        if request.files.getlist('files') == []:
            flash('No files part')
            return redirect(request.url)
        # print(request.files.getlist('files') is None)
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


@app.route('/delete_all')
@login_required
def delete_all():
    db.session.query(favorites).delete()
    db.session.query(note_file).delete()
    db.session.query(conspect_file).delete()
    db.session.query(File).delete()
    db.session.query(Note).delete()
    db.session.query(Conspect).delete()
    db.session.commit()
    return redirect(url_for('upload_conspects'))