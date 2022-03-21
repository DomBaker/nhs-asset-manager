from email import message
from wsgiref import validate
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, SubmitField
from wtforms.validators import InputRequired, Length, EqualTo

class RegForm(FlaskForm):
    """This is the Registration Form"""

    username = StringField('user_label', validators=[InputRequired(message="A username is requred"), Length(min= 4, max=30, message="Username must be between 4 and 30 characters")])
    password = PasswordField('password_label', validators=[InputRequired(message="A password is requred"), Length(min= 8, max=45, message="Password must be between 8 and 45 characters")])
    cfm_password = PasswordField('cfm_password_label', validators=[InputRequired(message="A username is requred"), EqualTo('password', message="passwords must match")])
    submit_button = SubmitField('Create')
