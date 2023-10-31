from flask import Flask, render_template, url_for, request, redirect

from config import app, db
from models import Note


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


@app.route('/notes')
def notes():
    endpoint = request.endpoint
    notes = Note.query.order_by(Note.data).all()
    return render_template('notes.html', notes=notes, endpoint=endpoint)


@app.route('/create_note', methods=['GET', 'POST'])
def create_note():
    if request.method == 'POST':
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']
        note = Note(title=title, intro=intro, text=text)
        try:
            db.session.add(note)
            db.session.commit()
            return redirect('/notes', code=302)
        except Exception as e:
            return 'При добавлении заметки произошла ошибка'
    else:
        endpoint = request.endpoint
        return render_template('create_note.html', endpoint=endpoint)


if __name__ == '__main__':
    app.run(debug=True)
