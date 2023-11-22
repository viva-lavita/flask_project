import os
import re
from typing import Optional
from views.notes import app, db
from models import File, Note, Conspect


def allowed_file(filename: str) -> bool:
    """Проверяет, является ли формат файла допустимым."""
    # print(filename.rsplit('.', 1)[1].lower())
    return ('.' in filename and filename.rsplit('.', 1)[1].lower()
            in app.config.get('ALLOWED_EXTENSIONS'))


def get_file_path(filename: str) -> str:
    """Возвращает путь файла по его имени."""
    return app.config.get('UPLOAD_FOLDER') + filename


def secure_filename(filename):
    # Удаление недопустимых символов
    filename = re.sub(r'[^\w\s.-@+]', '', filename)

    # Замена пробелов на подчеркивания
    filename = filename.replace(' ', '_')

    # Замена / на -
    filename = filename.replace('/', '-')

    return filename


def get_file(filename: str) -> Optional[File]:
    """
    Если файл существует, то возвращает его, иначе создает
    новый экземпляр модели.
    Дополнительно проверяет и корректирует имя файла.
    """
    if filename != '' and allowed_file(filename):
        # filename = secure_filename(filename)
        # original_filename = "Docker5 /боевая развертка + CI-CD.md"
        filename = secure_filename(filename)
        # print(processed_filename)  # Выведет: "Конспекты.md"
        existing_file = File.query.filter(File.name == filename).first()
        file = existing_file if existing_file else File(
            name=filename,
            path=get_file_path(filename)
        )
        return file


def add_at_note_and_save_files(files: list, note: Note) -> Note:
    """
    Добавляет файлы в Note и сохраняет их.
    """
    for uploaded_file in files:
        file = get_file(uploaded_file.filename)
        if file:
            if file.is_used_in_note(note):
                continue
            note.files.append(file)
            try:
                uploaded_file.save(app.config.get('UPLOAD_FOLDER') + file.name)
                db.session.add(file)
            except Exception as e:
                raise Exception(
                    f'При добавлении иллюстрации произошла ошибка: {e}'
                )
    return note


def add_at_conspects_and_save_files(files: list, user_id: int) -> list:
    """
    Массовая загрузка конспектов.
    Дополнительно добавляет их в Conspect.
    Возвращает список идентификаторов созданных конспектов.
    """
    conspect_ids = []
    for uploaded_file in files:
        file = get_file(uploaded_file.filename)
        # print(file.name)
        if file and check_md_file(file.name):
            conspect = create_conspect(file.name, user_id)
            conspect_ids.append(conspect.id)
            if conspect:
                conspect.files.append(file)
                try:
                    uploaded_file.save(
                        app.config.get('UPLOAD_FOLDER') + file.name
                    )
                    db.session.add(file)
                except Exception as e:
                    raise Exception(
                        f'При добавлении конспекта произошла ошибка: {e}'
                    )
    if conspect_ids:
        try:
            db.session.commit()
        except Exception as e:
            raise Exception(
                f'При добавлении одного из конспектов произошла ошибка: {e}'
            )
    return conspect_ids


def create_conspect(filename, user_id):
    """Создает конспект"""
    conspect = Conspect(name=filename,
                        user_id=user_id,)
    try:
        db.session.add(conspect)
        db.session.commit()
    except Exception as e:
        raise Exception(
            f'При добавлении конспекта произошла ошибка: {e}'
        )
    return conspect


def check_md_file(filename):
    if filename.rsplit('.', 1)[1].lower() == 'md':
        return True
