from flask import Flask, render_template, redirect, url_for
from passlib.hash import pbkdf2_sha256

from forms import *
from models import *

#config app
app = Flask(__name__)
app.secret_key = 'dom'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://diatkvddiwuhvr:2c168535c8d127354f6eb87e0a8ca63b400705f148eb34708fcdf653923f7b35@ec2-34-255-21-191.eu-west-1.compute.amazonaws.com:5432/d2fitfd02u1pu4'

database = SQLAlchemy(app)

@app.route("/", methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route("/register", methods=['GET', 'POST'])
def register():

    registration = RegForm()

    if registration.validate_on_submit():
        email = registration.email.data
        fname = registration.fname.data
        lname = registration.lname.data
        position = registration.position.data
        password = registration.password.data

        secure_password = pbkdf2_sha256.hash(password)

        #check existance
        user_object = User.query.filter_by(email=email).first()
        user = User(email=email, fname=fname, lname=lname, position=position, password=secure_password)

        database.session.add(user)
        #commit the changes to the database
        database.session.commit()
        
        return redirect(url_for('login'))

    return render_template('register.html', form=registration)

@app.route("/login", methods=['GET', 'POST'])
def login():

    login_form = LoginForm()

    if login_form.validate_on_submit():
        return render_template('dashboard.html')
    
    return render_template('login.html', form=login_form)

if __name__ == "__main__":
    app.run(debug=True)
