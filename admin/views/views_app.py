from flask import redirect, url_for
from flask_admin import AdminIndexView, BaseView, expose


class HomeView(BaseView):
    @expose('/')
    def go_to_index(self):
        return redirect(url_for('index'))


class DashBordView(AdminIndexView):
    @expose('/')
    def dashbord(self):
        return self.render('admin/dashbord.html')