# from flask import flash, render_template, request, redirect, url_for
# from flask_login import login_required, login_user, logout_user, current_user

from config import app, db

from views.app import *


if not app.debug:
    import logging
    from logging.handlers import SMTPHandler

    credentials = None
    if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
        credentials = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])

    mail_handler = SMTPHandler(
        (app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
        'no-reply@' + app.config['MAIL_SERVER'],
        app.config['ADMINS'],
        'NoteVi failure',
        credentials
    )
    mail_handler.setLevel(logging.ERROR)
    app.logger.addHandler(mail_handler)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
