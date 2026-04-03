from sqlalchemy.exc import IntegrityError

from eapp.models import Category, Product, User
import hashlib
from eapp import  db
import cloudinary.uploader
from flask import current_app
import re

def load_categories():
    return Category.query.all()

def load_products(cate_id=None, kw=None, page=None):
    query = Product.query

    if kw:
        query = query.filter(Product.name.contains(kw))

    if cate_id:
        query = query.filter(Product.category_id.__eq__(cate_id))

    if page:
        start = (page - 1) * current_app.config['PAGE_SIZE']
        query = query.slice(start, start + current_app.config['PAGE_SIZE'])

    return query.all()


def count_products():
    return Product.query.count()


def get_user_by_id(id):
    return User.query.get(id)

def auth_user(username, password):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    return User.query.filter(User.username==username,
                             User.password==password).first()

def add_user(name, username, password, avatar):
    if len(username.strip()) <5 :
        raise ValueError("user phai toi thieu 5 ky tu")
    if len(password.strip()) <8 :
        raise ValueError("Mat khau phai toi thieu 8 ky tu")
    if  not re.search(r'[0-9]',password.strip()):
        raise ValueError("Mat khau phai chua Ky so")
    if not re.search(r'[a-zA-Z]',password.strip()):
        raise ValueError('Mat khau phai chua ky tu')
    if User.query.filter(User.username.__eq__(username.strip())).first():
        raise ValueError('User name da ton tai')

    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    u = User(name=name.strip(), username=username.strip(), password=password)
    if avatar:
        res = cloudinary.uploader.upload(avatar)
        u.avatar = res.get("secure_url")

    db.session.add(u)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        raise Exception('Username đã tồn tại!')

