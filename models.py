from datetime import datetime

# from flask_login import LoginManager, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from config import db, login_manager


@login_manager.user_loader
def user_loader(id: int):
    return db.session.query(User).get(id)


roles_group = db.Table(
    'roles_group',
    db.Column('role_id', db.Integer, db.ForeignKey('role.id')),
    db.Column('group_id', db.Integer, db.ForeignKey('group.id'))
)


group_users = db.Table(
    'group_users',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('group_id', db.Integer, db.ForeignKey('group.id'))
)


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)

    def __str__(self):
        return self.name


class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    roles = db.relationship('Role',
                            secondary=roles_group,
                            backref=db.backref('groups',
                                               lazy='dynamic'))
    users = db.relationship('User',
                            secondary=group_users,
                            backref=db.backref('groups',
                                               lazy='dynamic'))

    def __str__(self):
        return self.name


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(
        db.String(64), index=True, unique=True, nullable=False
    )
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    notes = db.relationship('Note',
                            backref='author',
                            lazy='dynamic',
                            cascade='all, delete')
    # roles = db.relationship('Role', secondary=roles_users,
    #                         backref=db.backref('users', lazy='dynamic'))
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_on = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    conspects = db.relationship('Conspect',
                                backref='author',
                                lazy='dynamic',
                                cascade='all, delete'
                                )
    name = db.Column(db.String(100))
    surname = db.Column(db.String(100))
    birth_date = db.Column(db.Date)
    phone = db.Column(db.String(100))
    city = db.Column(db.String(200))
    profession = db.Column(db.String(100))
    site = db.Column(db.String(100))
    github = db.Column(db.String(100))

    def __repr__(self):
        return '<User %r>' % self.username

    def set_password(self, password):
        """ Генерация хэша пароля """
        self.password_hash = generate_password_hash(password)

    def check_password(self,  password):
        """ Проверка пароля """
        return check_password_hash(self.password_hash, password)

    def is_favorite(self, note) -> bool:
        """Проверяет, является ли заметка избранной."""
        if self.favorite_notes is None:
            return False
        return self.favorite_notes and note in set(self.favorite_notes)

    def is_favorite_conspect(self, conspect):
        """ Проверка конспекта на избранное """
        if not self.favorite_conspects:
            return False
        return conspect in self.favorite_conspects

    def is_author(self, instance):
        """ Проверка на авторство. """
        return self.id == instance.user_id

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    @property
    def roles(self):
        _roles = set()
        for group in self.groups:
            for role in group.roles:
                _roles.add(role)
        return _roles

    def has_role(self, role):
        if isinstance(role, str):
            role = Role.query.filter_by(name=role.lower()).first()
        #
        if not role:
            return False
        #
        return role in self.roles

    def has_roles(self, *roles_seq):
        def _has_one_role(*_roles):
            # checks if the user has at least one role of many (OR Gate)
            for _role in _roles:
                if self.has_role(_role):
                    return True
            return False

        for role_value in roles_seq:
            if isinstance(role_value, (list, tuple, set)):
                if not _has_one_role(*role_value):
                    return False
            elif not self.has_role(role_value):
                return False
        return True

    def get_id(self):
        return self.id

    @property
    def is_admin(self):
        return self.has_role('admin')

    def __unicode__(self):
        return self.username

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
    text = db.Column(db.Text)
    user_id = db.Column(db.Integer,
                        db.ForeignKey('user.id'))
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


class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    path = db.Column(db.String(255), nullable=False)
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)

    def __repr__(self):
        return '<File %r>' % self.id

    def is_used_in_note(self, note):
        if not self.notes:
            return False
        return note in self.notes

    def is_used_in_conspect(self):
        if not self.conspects:
            return False
        return self.conspects


# M2M конспект, файл .md для отрисовки
conspect_file = db.Table(
    'conspect_file',
    db.Column(
        'conspect_id',
        db.Integer,
        db.ForeignKey('conspect.id'),
        primary_key=True
    ),
    db.Column(
        'file_id',
        db.Integer,
        db.ForeignKey('file.id'),
        primary_key=True
    )
)

# M2M иллюстрация конспекта
conspect_image = db.Table(
    'conspect_image',
    db.Column(
        'conspect_id',
        db.Integer,
        db.ForeignKey('conspect.id')
    ),
    db.Column(
        'file_id',
        db.Integer,
        db.ForeignKey('file.id')
    )
)


# M2M избранное
favorites_conspect = db.Table(
    'favorites_conspect',
    db.Column(
        'conspect_id',
        db.Integer,
        db.ForeignKey('conspect.id'),
        primary_key=True
    ),
    db.Column(
        'user_id',
        db.Integer,
        db.ForeignKey('user.id'),
        primary_key=True
    )
)


class Conspect(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, default='Not_name')
    files = db.relationship('File',
                            secondary='conspect_file',
                            lazy='subquery',
                            backref=db.backref('conspects',
                                               lazy=True))
    add_date = db.Column(db.Date(), default=datetime.utcnow)
    public = db.Column(db.String(8), default=None)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    intro = db.Column(db.String(200), nullable=False, default=' ')
    favorites = db.relationship('User',
                                secondary='favorites_conspect',
                                backref=db.backref('favorite_conspects',
                                                   lazy=True),
                                lazy='subquery')
    images = db.relationship('File',
                             secondary='conspect_image',
                             lazy='subquery',
                             backref=db.backref('img_conspects',
                                                lazy=True))

    def __repr__(self):
        return '<Conspect %r>' % self.id

    @classmethod
    def get_by_id(cls, id_) -> 'Conspect':
        """
        Кастомный метод запроса объекта модели по id.
        Model.get_by_id(id)
        """
        return cls.query.session.get(cls, id_)

    @classmethod
    def get_public_conspects(cls):
        return (cls.query.filter_by(public='on')
                         .order_by(cls.id.desc())
                         .all())
