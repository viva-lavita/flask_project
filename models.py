from datetime import datetime

from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    role = db.Column(db.String(128))

    def __repr__(self):
        return '<User %r>' % self.name


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    intro = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(20), nullable=False, default='N/A')
    data = db.Column(db.Date, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return '<Article %r>' % self.id  # обьект и его id 