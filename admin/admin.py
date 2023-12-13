from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from .views.views_app import DashBordView, HomeView
from new_main import app, db
from models import User, Note, File, Conspect, Group, Role


admin = Admin(app, name='NoteVi', template_mode='bootstrap3', index_view=DashBordView())

admin.add_view(ModelView(User, db.session, name='Пользователи'))
admin.add_view(ModelView(Note, db.session, name='Заметки'))
admin.add_view(ModelView(File, db.session, name='Файлы'))
admin.add_view(ModelView(Conspect, db.session, name='Конспекты'))
admin.add_view(ModelView(Group, db.session, name='Группы'))
admin.add_view(ModelView(Role, db.session, name='Роли'))
admin.add_view(HomeView(name='Сайт'))
