import os

from flask import (
    render_template, redirect, flash, request,
    send_from_directory, url_for)
from werkzeug.utils import secure_filename

from config import app, db, cache
from .notes import *
from .users import *
from .test_api import *


def allowed_file(filename):
    return ('.' in filename and filename.rsplit('.', 1)[1].lower()
            in app.config.get('ALLOWED_EXTENSIONS'))


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
    return render_template('upload.html')


@app.route('/downloads/<name>', methods=['GET'])
def download_file(name):
    return send_from_directory(app.config.get("UPLOAD_FOLDER"), name)


@app.errorhandler(404)
def not_found_error(error):
    error = '404'
    return render_template('404.html', error=error), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('404.html'), 500


@app.errorhandler(502)
def bad_gateway(error):
    db.session.rollback()
    error = '502'
    return render_template('404.html', error=error), 502


@app.route('/index')
@app.route('/')
@cache.cached(timeout=60)
def index():
    endpoint = request.endpoint
    return render_template('index.html', endpoint=endpoint)


@app.route('/about')
def about():
    endpoint = request.endpoint
    return render_template('about.html', endpoint=endpoint)


@app.route('/contact')  # переписать
def contact():
    endpoint = request.endpoint
    return render_template('contact.html', endpoint=endpoint)


@app.route('/conditions')
def conditions():
    return render_template('site_stub.html')


@app.route('/bot')
def bot():
    return render_template('site_stub.html')


@app.route('/telegram')
def telegram():
    return render_template('site_stub.html')
