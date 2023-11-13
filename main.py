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

# Точка входа. Можно убрать, но нужно тогда прописать
# команды для создания и миграций бд + прописать в
# докерфайле или в компоузе комманду старта приложения.
# Сейчас там указана точка входа.
if __name__ == '__main__':  # для разработки.
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000)
