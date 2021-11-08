from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class CreateForm(FlaskForm):
    title = StringField(
        'Title',
        [DataRequired()]
    )
    description = StringField(
        'Description',
        [DataRequired()]
    )
    price = IntegerField(
        'Price',
        [DataRequired()]
    )
    submit = SubmitField('Submit')


class SignupForm(FlaskForm):
    email = StringField(
        'Email',
        [
            Email(message='Не корректный email'),
            DataRequired(message='Введите email')
        ]
    )
    username = StringField(
        'Username',
        [
            DataRequired(message='Введите имя пользователя'),
            Length(min=5)
        ]
    )
    name = StringField()
    password = PasswordField(
        'Password',
        [
            DataRequired(message='Введите пароль'),
            Length(min=6, message='Пароль должен быть от 6 символов')
        ]
    )
    confirm_password = PasswordField(
        'Repeat Password',
        [
            EqualTo('password', message='Пароли не совпадают')
        ]
    )
    submit = SubmitField('Submit')


class LoginForm(FlaskForm):

    email = StringField(
        'Email',
        [
            DataRequired(message='Введите email'),
            Email(message='Не корректный email')
        ]
    )
    password = PasswordField(
        'Password',
        [
            DataRequired(message='Введите пароль'),
            Length(min=6, message='Пароль должен быть от 6 символов')
        ]
    )
    submit = SubmitField('Submit')
