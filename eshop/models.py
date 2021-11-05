from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from . import db


class Main:
    def add_to(self):
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except Exception as e:
            print(e)
            return False

    def delete_from(self):
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except Exception as e:
            print(e)
            return False


class User(UserMixin, db.Model, Main):

    __tablename__ = 'eshop_User'

    id = db.Column(
        db.Integer,
        primary_key=True
    )
    email = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )
    username = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )
    name = db.Column(
        db.String(200)
    )
    password = db.Column(
        db.String(200),
        primary_key=False,
        unique=False,
        nullable=False
    )
    reg_date = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    def __init__(self, email, username, name):
        self.email = email
        self.username = username
        self.name = name

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(
            password,
            method='sha256'
        )

    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)


class Product(db.Model, Main):

    __tablename__ = 'eshop_Product'

    id = db.Column(
        db.Integer,
        primary_key=True
    )
    title = db.Column(
        db.String(100),
        nullable=False
    )
    price = db.Column(
        db.Integer,
        nullable=False
    )
    onStorage = db.Column(
        db.Boolean,
        default=True
    )
    text = db.Column(
        db.Text,
        nullable=False
    )
    creator = db.Column(
        db.String(100),
        db.ForeignKey('eshop_User.email')
    )

    def __init__(self, title, price, creator):
        self.title = title
        self.price = price
        self.creator = creator
        self.text = 'text'

    def __repr__(self):
        return f'{self.title}'

