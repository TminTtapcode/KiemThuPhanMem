from tkinter.font import names

from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from eapp.models import Category, Product, UserRole
from eapp import db, app
from flask_login import current_user, logout_user
from flask_admin import BaseView, expose
from flask import redirect

class AdminView(ModelView):
    def is_accessible(self) -> bool:
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN

class ProductView(AdminView):
    column_list = ['id', 'name', 'price', 'active', 'category_id']
    column_searchable_list = ['name']
    column_filters = ['id', 'name', 'price']
    can_export = True
    edit_modal = True
    column_editable_list = ['name']
    page_size = 30


class LogoutView(BaseView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/admin')

    def is_accessible(self) -> bool:
        return current_user.is_authenticated


admin = Admin(app=app, name="e-Commerce's Admin")

admin.add_view(AdminView(Category, db.session))
admin.add_view(ProductView(Product, db.session))
admin.add_view(LogoutView(name='Đăng xuất'))
