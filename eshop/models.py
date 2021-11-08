from datetime import datetime
from flask_security import UserMixin, RoleMixin, SQLAlchemyUserDatastore
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


roles_users = db.Table(
                        'roles_users',
                        db.Column('user_id', db.Integer(), db.ForeignKey('eshop_User.id')),
                        db.Column('role_id', db.Integer(), db.ForeignKey('eshop_Role.id'))
                      )


class User(db.Model, UserMixin, Main):

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
    active = db.Column(db.Boolean(), default=True)
    roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))

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


class Role(db.Model, RoleMixin, Main):

    __tablename__ = 'eshop_Role'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(255))


user_datastore = SQLAlchemyUserDatastore(db, User, Role)


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
    description = db.Column(
        db.Text,
        nullable=False
    )
    creator = db.Column(
        db.String(100),
        db.ForeignKey('eshop_User.email')
    )

    def __init__(self, title, description, price, creator):
        self.title = title
        self.description = description
        self.price = price
        self.creator = creator

    def __repr__(self):
        return f'{self.title}'

