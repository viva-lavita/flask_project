# from flask_admin import create_admin
# from flask_security import UserMixin, RoleMixin
# from flask_admin import Admin
# from flask_security import Security, SQLAlchemyUserDatastore
from datetime import datetime
from flask_login import LoginManager, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import current_user

from config import db, login_manager


# roles_users = db.Table(
#     'roles_users',
#     db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
#     db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
# )


# class Role(db.Model, RoleMixin):
#     id = db.Column(db.Integer(), primary_key=True)
#     name = db.Column(db.String(80), unique=True)
#     description = db.Column(db.String(255))


favorites = db.Table(
    'favorites',
    db.Column(
        'note_id', db.Integer, db.ForeignKey('note.id'), primary_key=True
    ),
    db.Column(
        'usser_id', db.Integer, db.ForeignKey('user.id'), primary_key=True
    )
)

note_file = db.Table(
    'note_file',
    db.Column(
        'note_id', db.Integer, db.ForeignKey('note.id'), primary_key=True
    ),
    db.Column(
        'file_id', db.Integer, db.ForeignKey('file.id'), primary_key=True
    )
)


@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).get(user_id)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(
        db.String(64), index=True, unique=True, nullable=False
    )
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    notes = db.relationship('Note', backref='author', lazy='dynamic')
    # roles = db.relationship('Role', secondary=roles_users,
    #                         backref=db.backref('users', lazy='dynamic'))
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_on = db.Column(
        db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow
    )
    is_active = db.Column(db.Boolean(), default=True)

    def __repr__(self):
        return '<User %r>' % self.username

    def set_password(self, password):
        """ Генерация хэша пароля """
        self.password_hash = generate_password_hash(password)

    def check_password(self,  password):
        """ Проверка пароля """
        return check_password_hash(self.password_hash, password)

    def is_favorite(self, note):
        """ Проверка заметки на избранное """
        if not self.favorite_notes:
            return False
        return note in self.favorite_notes

    def is_author(self, note):
        """ Проверка заметки на автора """
        return self.id == note.user_id

    @classmethod
    def get_by_id(cls, id_) -> 'User':
        """
        Кастомный метод запроса объекта модели по id.
        Model.get_by_id(id)
        """
        return cls.query.session.get(cls, id_)


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False, default=' ')
    intro = db.Column(db.String(200), nullable=False, default=' ')
    text = db.Column(db.Text, nullable=False, default=' ')
    user_id = db.Column(db.Integer,
                        db.ForeignKey('user.id'),)
                        # nullable=False,
                        # default=1)
                        # default=current_user.id)
    data = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    favorites = db.relationship('User',
                                secondary='favorites',
                                backref=db.backref('favorite_notes',
                                                   lazy=True),
                                lazy='subquery')
    public = db.Column(db.String(8), default=None)
    files = db.relationship('File',
                            secondary='note_file',
                            lazy='subquery',
                            backref=db.backref('notes',
                                               lazy=True))

    def __repr__(self):
        return '<Article %r>' % self.id

    @classmethod
    def get_by_id(cls, id_) -> 'Note':
        """
        Кастомный метод запроса объекта модели по id.
        Model.get_by_id(id)
        """
        return cls.query.session.get(cls, id_)


class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    path = db.Column(db.String(255), nullable=False)
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)

    def __repr__(self):
        return '<File %r>' % self.id

    def is_used(self, note):
        if not self.notes:
            return False
        return note in self.notes
