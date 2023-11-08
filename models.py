# from flask_admin import create_admin
# from flask_security import UserMixin, RoleMixin
# from flask_admin import Admin
# from flask_security import Security, SQLAlchemyUserDatastore
from datetime import datetime
from flask_login import LoginManager, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

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


@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).get(user_id)


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(
        db.String(64), index=True, unique=True, nullable=False
    )
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    notes = db.relationship('Note', backref='author', lazy='dynamic')
    # roles = db.relationship('Role', secondary=roles_users,
    #                         backref=db.backref('users', lazy='dynamic'))
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_on = db.Column(
        db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow
    )

    def __init__(self, email, username):
        self.username = username
        self.email = email
        self.active = True
        self.confirmed_at = datetime.utcnow()

    def __repr__(self):
        return '<User %r>' % self.username

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self,  password):
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
                        db.ForeignKey('user.id'),
                        nullable=False,
                        default=1)
    data = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    favorites = db.relationship('User',
                                secondary='favorites',
                                backref=db.backref('favorite_notes',
                                                   lazy=True),
                                lazy='subquery')
    public = db.Column(db.String(8), default=None)


    def __repr__(self):
        return '<Article %r>' % self.id  # обьект и его id

    @classmethod
    def get_by_id(cls, id_) -> 'Note':
        """
        Кастомный метод запроса объекта модели по id.
        Model.get_by_id(id)
        """
        return cls.query.session.get(cls, id_)
