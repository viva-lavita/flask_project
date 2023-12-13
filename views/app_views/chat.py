from flask import request, render_template, redirect, url_for, session

from utils.generate_room_code import generate_room_code
from views import app


rooms = {}


@app.route('/chat', methods=["GET", "POST"])
def home():
    session.clear()

    if request.method == "POST":
        name = request.form.get('name')
        create = request.form.get('create', False)
        code = request.form.get('code')
        join = request.form.get('join', False)

        if not name:
            return render_template(
                'home.html', error="Name is required", code=code
            )

        if create is not False:
            room_code = generate_room_code(6, list(rooms.keys()))
            new_room = {
                'members': 0,
                'messages': []
            }
            rooms[room_code] = new_room

        if join is not False:
            # no code
            if not code:
                return render_template(
                    'home.html',
                    error="Please enter a room code to enter a chat room",
                    name=name
                )
            # invalid code
            if code not in rooms:
                return render_template(
                    'home.html',
                    error="Room code invalid",
                    name=name
                )

            room_code = code

        session['room'] = room_code
        session['name'] = name
        return redirect(url_for('app.room'))
    else:
        return render_template('home.html')


@app.route('/room')
def room():
    room = session.get('room')
    name = session.get('name')

    if name is None or room is None or room not in rooms:
        return redirect(url_for('app.home'))

    messages = rooms[room]['messages']
    return render_template(
        'room.html', room=room, user=name, messages=messages
    )
