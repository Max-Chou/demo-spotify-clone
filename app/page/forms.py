from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class SignupForm(FlaskForm):
    first_name = StringField('First Name', validators=[
        DataRequired(),
        Length(max=25)
    ])

    last_name = StringField('Last Name', validators=[
        DataRequired(),
        Length(max=25)
    ])

    username = StringField('Username', validators=[
        DataRequired(),
        Length(max=25)
    ])

    email = StringField('Email', validators=[
        DataRequired(),
        Length(max=100),
        Email(),
        EqualTo('email2', message='Emails must match.')
    ])
    email2 = StringField('Confirm email')
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(8, 16),
        EqualTo('password2', message='Passwords must match')
    ])
    password2 = PasswordField('Confirm Password')


class SigninForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(),
    ])

    password = PasswordField('Password', validators=[
        DataRequired()
    ])
