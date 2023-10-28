from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)


@app.route('/')
@app.route('/index')
def index():
    return 'Hello World!'


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contact/<string:name>')
def contact(name):
    return render_template('contact.html', name=name)


if __name__ == '__main__':
    with app.app_context():
    # Create the database tables
        db.create_all()
    app.run(debug=True)
