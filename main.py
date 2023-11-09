from config import app, db
from views.app import *


if not app.debug:
    import logging
    from logging.handlers import SMTPHandler

    mail_handler = SMTPHandler(
        mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
        fromaddr=app.config['SECURITY_EMAIL_SENDER'],
        toaddrs=app.config['MAIL_USERNAME'],
        subject='Error occurred!',
        credentials=(app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD']),
        secure=()
    )
    mail_handler.setLevel(logging.ERROR)
    logger = logging.getLogger()
    logger.addHandler(mail_handler)

file_handler = logging.FileHandler('app.log')
file_handler.setLevel(logging.ERROR)

# Создание форматтера для указания формата записи логов
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
file_handler.setFormatter(formatter)

# Получение корневого логгера
logger = logging.getLogger()
logger.addHandler(file_handler)

if __name__ == '__main__':
    # with app.app_context():
    #     db.create_all()
    app.run(debug=True)
