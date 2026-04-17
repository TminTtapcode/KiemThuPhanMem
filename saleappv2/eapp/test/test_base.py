import pytest
from flask import Flask
from eapp import db
from eapp.index import register_routers
from eapp.models import Product


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config['PAGE_SIZE'] = 2
    app.config['TESTING'] = True
    app.secret_key="asdasdasdasdsadasdasdasd"
    db.init_app(app)

    register_routers(app=app)
    return app


@pytest.fixture
def test_app():
    app = create_app()

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def test_client(test_app):
    return test_app.test_client()


@pytest.fixture
def test_session(test_app):
    yield db.session


@pytest.fixture
def sample_products(test_session):
    p1 = Product(name = 'iPhone 7', price =50 , category_id =1)
    p2 = Product(name='Galaxy 7', price=80, category_id=1)
    p3 = Product(name='iPad 7 def', price=50, category_id=2)
    p4 = Product(name='iPhone 7 abc', price=50, category_id=2)
    p5 = Product(name='iPhone 7 EDF', price=50, category_id=2)

    test_session.add_all([p1,p2,p3,p4,p5])
    test_session.commit()

    return [p1,p2,p3,p4,p5]

@pytest.fixture
def mock_cloundinary(monkeypatch):
    def fake_upload(file):
        return {'secure_url': 'https://fake-image.png'}
    monkeypatch.setattr('cloudinary.uploader.upload', fake_upload)