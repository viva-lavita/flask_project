import sys
from config import app, db
from views.app import *


# Отправка логирования на почту
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

# Настройка файла логирования !!!!!!!!!!добавить ограничение размера!!!!!!!!!
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


# для локального запуска
if __name__ == '__main__': 
    with app.app_context():
        try:
            db.create_all()
            sys.stdout.write('База данных обновлена')
        except Exception as e:
            sys.stdout.write(f'Ошибка создания БД: + {e}')
    app.run(host='0.0.0.0', port=5000)
