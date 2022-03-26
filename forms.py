from email import message
from wsgiref import validate
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, SubmitField
from wtforms.validators import InputRequired, Length, EqualTo, ValidationError

from models import User


#This is a custom validator, I have included two different methods of creating and using custom validators to show different approaches in my app
# Typically you would define the function for a validator out the class if it was going to be reused. (This isn't reused but here to show my understanding)
def invalid_creds(form, field):
    """ Check email and password """

    email_entered = form.email.data
    password_entered = field.data

    user_object = User.query.filter_by(email=email_entered).first()
    if user_object is None:
        raise ValidationError("Email or password is incorrect")
    elif password_entered != user_object.password:
        raise ValidationError("Email or password is incorrect")
        

class RegForm(FlaskForm):
    """This is the Registration Form"""

    email = EmailField('email_label', validators=[InputRequired(message="An email is required to register")])
    fname = StringField('fname_label', validators=[InputRequired(message="Please input your first name")])
    lname = StringField('lname_label', validators=[InputRequired(message="Please input your last name")])
    position = StringField('position_label', validators=[InputRequired(message="Please input your job role")])
    password = PasswordField('password_label', validators=[InputRequired(message="A password is requred"), Length(min= 8, max=150, message="Password must be between 8 and 45 characters")])
    cfm_password = PasswordField('cfm_password_label', validators=[InputRequired(message="A username is requred"), EqualTo('password', message="passwords must match")])
    submit_button = SubmitField('Create Account')
    #Second custom validator
    def validate_email(self, email):
        user_object = User.query.filter_by(email=email.data).first()
        if user_object:
            raise ValidationError("Email is already used, Please try logging in")


class LoginForm(FlaskForm):
    """ This is the login form """

    email = EmailField('email_label', validators=[InputRequired(message="Your email is required to login")])
    password = StringField('password_label', validators=[InputRequired(message="Your password is required to login"), invalid_creds])
    submit_button = SubmitField('Login')
