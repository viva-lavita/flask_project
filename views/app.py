from flask import render_template, request, url_for

from config import app, db, cache
from .notes import *
from .users import *
from .test_api import *


@app.errorhandler(404)
def not_found_error(error):
    error = '404'
    return render_template('404.html', error=error), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('404.html'), 500


@app.route('/')
@app.route('/index')
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
