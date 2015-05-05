from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, TextAreaField,validators,TextField,PasswordField
from wtforms.validators import DataRequired, Length
from .models import User

class RegistrationForm(Form):
    username = TextField('Username', [validators.Length(min=4, max=20)])
    email = TextField('Email Address', [validators.Length(min=6, max=50)])
    password = PasswordField('New Password', [
        validators.Required(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    
class LoginForm(Form):
    username = TextField('Username', [validators.Length(min=4, max=20)])
    # email = StringField('openid', validators=[DataRequired()])

    password = PasswordField('New Password', [
        validators.Required(),])
