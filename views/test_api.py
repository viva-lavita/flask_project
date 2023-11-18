from flask import request, jsonify
import requests

from .app import app



@app.route("/universities")
def get_universities():
    API_URL = "http://universities.hipolabs.com/search?country="
    search = request.args.get('country')
    r = requests.get(f"{API_URL}{search}")
    return jsonify(r.json())


# def create_note():
#     if request.method == 'POST':
#         note = Note(
#             title=request.form['title'],
#             intro=request.form['intro'],
#             text=request.form['text'],
#             user_id=current_user.id,
#             public=request.form.get('public')
#         )
#         try:
#             note = add_and_save_files(request.files.getlist('files'), note)
#             db.session.add(note)
#             db.session.commit()
#         except Exception as e:
#             return f'При добавлении заметки произошла ошибка: {e}'

#         return redirect(url_for('note', id=note.id))
#     else:
#         endpoint = request.endpoint
#         return render_template('create_note.html', endpoint=endpoint)