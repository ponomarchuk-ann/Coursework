"""
В данном файле описаны две формы - форма для регистрации пользователя и форма для его авторизации
"""

from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, EqualTo


# форма для регистрации состоит из трёх полей, ни одно из которых не может быть пустым; четвёртое поле - кнопка "Register"
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()], render_kw={'class': 'form-control'})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={'class': 'form-control'})
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')], render_kw={'class': 'form-control'})
    submit = SubmitField('Register', render_kw={'class': 'btn btn-success'})


# форма для авторизации состоит из трёх полей: имя пользователя, пароль и кнопка "запомнить меня", которая позволяет
# избежать повторного ввода информации при последующих посещениях сайта; четвёртое поле - кнопка "Login"
class LoginForm(FlaskForm):
    username = StringField('Username', render_kw={'class': 'form-control'})
    password = PasswordField('Password', render_kw={'class': 'form-control'})
    remember_me = BooleanField('remember_me')
    submit = SubmitField('Login', render_kw={'class': 'btn btn-success'})
