import os
from typing import Optional
from werkzeug.utils import secure_filename
from views.notes import app, db
from models import File


def allowed_file(filename):
    """Проверяет, является ли формат файла допустимым."""
    return ('.' in filename and filename.rsplit('.', 1)[1].lower()
            in app.config.get('ALLOWED_EXTENSIONS'))


def get_file_path(filename) -> str:
    """Возвращает путь файла по его имени."""
    return app.config.get('UPLOAD_FOLDER') + filename


def get_file(filename) -> Optional[File]:
    """
    Если файл существует, то возвращает его, иначе создает
    новый экземпляр модели.
    Дополнительно проверяет и корректирует имя файла.
    """
    if filename != '' and allowed_file(filename):
        filename = secure_filename(filename)
        existing_file = File.query.filter(File.name == filename).first()
        file = existing_file if existing_file else File(
            name=filename,
            path=get_file_path(filename)
        )
        return file


def add_and_save_files(files, note):
    """
    Добавляет файлы в заметку и сохраняет их.
    """
    for uploaded_file in files:
        file = get_file(uploaded_file.filename)
        if file:
            note.files.append(file)
            try:
                uploaded_file.save(app.config.get('UPLOAD_FOLDER') + file.name)
                db.session.add(file)
            except Exception as e:
                raise Exception(
                    f'При добавлении иллюстрации произошла ошибка: {e}'
                )
    return note
