from flask import render_template, request, url_for

from config import app, db
from .notes import *
from .users import *


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
def index():
    endpoint = request.endpoint
    return render_template('index.html', endpoint=endpoint)


@app.route('/about')
def about():
    endpoint = request.endpoint
    return render_template('about.html', endpoint=endpoint)


@app.route('/contact/<string:name>')  # переписать
def contact(name):
    endpoint = request.endpoint
    return render_template('contact.html', name=name, endpoint=endpoint)
