from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, SubmitField, SelectField, IntegerField
from wtforms.validators import InputRequired, Length, EqualTo, ValidationError
from passlib.hash import pbkdf2_sha256

from models import User, Assets


#This is a custom validator, I have included two different methods of creating and using custom validators to show different approaches in my app
# Typically you would define the function for a validator out the class if it was going to be reused. (This isn't reused but here to show my understanding)
def invalid_creds(form, field):
    """ Check email and password """

    email_entered = form.email.data
    password_entered = field.data

    user_object = User.query.filter_by(email=email_entered).first()
    if user_object is None:
        raise ValidationError("Enter a registered email and password")
    elif not pbkdf2_sha256.verify(password_entered, user_object.password):
        raise ValidationError("Email or password is incorrect")
        

class UserForm(FlaskForm):
    """This is the Registration Form"""

    email = EmailField('email_label', validators=[InputRequired(message="An email is required to register")])
    fname = StringField('fname_label', validators=[InputRequired(message="Please input your first name")])
    lname = StringField('lname_label', validators=[InputRequired(message="Please input your last name")])
    position = StringField('position_label', validators=[InputRequired(message="Please input your job role")])
    password = PasswordField('password_label', validators=[InputRequired(message="A password is requred"), Length(min= 8, max=150, message="Password must be between 8 and 45 characters")])
    cfm_password = PasswordField('cfm_password_label', validators=[InputRequired(message="A username is requred"), EqualTo('password', message="passwords must match")])
    is_admin = SelectField("account_type_label", choices=[('0', 'Standard'),('1', 'Admin')], validate_choice=False, coerce=int)
    submit_button = SubmitField('Submit')
    #Second custom validator
    def validate_email(self, email):
        user_object = User.query.filter_by(email=email.data).first()
        if user_object:
            raise ValidationError("Email is already used, Please try logging in")


class LoginForm(FlaskForm):
    """ This is the login form """

    email = EmailField('email_label', validators=[InputRequired(message="Your email is required to login")])
    password = PasswordField('password_label', validators=[InputRequired(message="Your password is required to login"), invalid_creds])
    submit_button = SubmitField('Login')


class UpdateForm(FlaskForm):
    """This is the Update Record Form"""

    fname = StringField('fname_label', validators=[InputRequired(message="Please input your first name")])
    lname = StringField('lname_label', validators=[InputRequired(message="Please input your last name")])
    position = StringField('position_label', validators=[InputRequired(message="Please your new position")])
    password = PasswordField('password_label', validators=[Length(min= 8, max=150, message="Password must be between 8 and 45 characters")])
    cfm_password = PasswordField('cfm_password_label', validators=[EqualTo('password', message="passwords must match")])
    submit_button = SubmitField('Update Account')


# ASSET FORMS ---------------------------------------------------------------------------------------------------------------------------------------------

class AddAsset(FlaskForm):
    asset_name = StringField('asset_name_label', validators=[InputRequired(message="Please input an asset name")])
    owner_id = IntegerField('owner_id_label', validators=[InputRequired(message="Please Input a valid owner id")])
    asset_type = SelectField("asset_type_label", choices=[('Laptop'),('Mobile'),('Other')], validate_choice=True)
    serial_number = IntegerField('serial_number_label', validators=[InputRequired(message="Please input the asset serial number")])
    submit_button = SubmitField('Add asset')

    def validate_serial_number(self, serial_number):
        asset_object = Assets.query.filter_by(serial_number=serial_number.data).first()
        if asset_object:
            raise ValidationError("Serial number already used, please make sure it is correct")
    
    def validate_owner_id(self, owner_id):
        user_object = User.query.filter_by(id=owner_id.data).first()
        if not user_object:
            raise ValidationError("This user id is invalid, please check that this user exists")

