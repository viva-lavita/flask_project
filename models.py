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


@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).get(user_id)


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    notes = db.relationship('Note', backref='author', lazy='dynamic')
    # roles = db.relationship('Role', secondary=roles_users,
    #                         backref=db.backref('users', lazy='dynamic'))
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_on = db.Column(db.DateTime(), default=datetime.utcnow,  onupdate=datetime.utcnow)

    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.active = True
        self.confirmed_at = datetime.utcnow()

    def __repr__(self):
        return '<User %r>' % self.username

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self,  password):
        return check_password_hash(self.password_hash, password)

    @classmethod
    def get_by_id(cls, id_) -> 'User':
        """
        Кастомный метод запроса объекта модели по id.
        Model.get_by_id(id)
        """
        return cls.query.session.get(cls, id_)


# admin = create_admin(app, db.session, User)
# admin.create_admin(username='admin', password='password')

# user_datastore = SQLAlchemyUserDatastore(db, User, Role)
# security = Security(app, user_datastore)
# admin = Admin(app, name='Example', template_mode='bootstrap3')


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    intro = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer,
                        db.ForeignKey('user.id'),
                        nullable=False,
                        default=1)
    data = db.Column(db.Date, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return '<Article %r>' % self.id  # обьект и его id

    @classmethod
    def get_by_id(cls, id_) -> 'Note':
        """
        Кастомный метод запроса объекта модели по id.
        Model.get_by_id(id)
        """
        return cls.query.session.get(cls, id_)
