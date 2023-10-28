from flask import Flask, render_template, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)


@app.route('/')
@app.route('/index')
def index():
    endpoint = request.endpoint
    return render_template('index.html', endpoint=endpoint)


@app.route('/about')
def about():
    endpoint = request.endpoint
    return render_template('about.html', endpoint=endpoint)


@app.route('/contact/<string:name>')
def contact(name):
    endpoint = request.endpoint
    return render_template('contact.html', name=name, endpoint=endpoint)


if __name__ == '__main__':
    app.run(debug=True)
