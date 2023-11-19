import markdown
import os
from flask import flash, render_template, request, redirect, url_for

from config import app, db
from models import File
from utils.files_utils import allowed_file, secure_filename


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
            # return redirect(url_for('download_file', name=filename))
            return redirect(url_for('index'), code=302)
        else:
            flash('Allowed file types are txt, pdf, png, jpg, jpeg, gif, md')
            return redirect(request.url)
    return render_template('upload.html')
