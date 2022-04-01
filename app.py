from flask import Flask, render_template, redirect, url_for
from flask_login import LoginManager, login_user, current_user, logout_user

from forms import *
from models import *

#config app
app = Flask(__name__)
#needs some kind of security on this
app.secret_key = 'dom'
#need to use some form of security on this 
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://diatkvddiwuhvr:2c168535c8d127354f6eb87e0a8ca63b400705f148eb34708fcdf653923f7b35@ec2-34-255-21-191.eu-west-1.compute.amazonaws.com:5432/d2fitfd02u1pu4'
database = SQLAlchemy(app)

login = LoginManager(app)
login.init_app(app)

#Used to track which user is logged in.
@login.user_loader
def load_user(id):
    return User.query.get(int(id))

#ROUTES

@app.route("/", methods=['GET', 'POST'])
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    return redirect(url_for('login'))

#Splash route for displaying more use friendly login required type page.
@app.route("/splash", methods=['GET', 'POST'])
def splash():
    return render_template('splash.html')

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
        user_object = User.query.filter_by(email=login_form.email.data).first()

        login_user(user_object)
        return redirect(url_for('dashboard'))
    
    return render_template('login.html', form=login_form)

@app.route("/dashboard", methods=['GET', 'POST'])
def dashboard():

    if not current_user.is_authenticated:
        return redirect(url_for('splash'))

    return render_template('dashboard.html')

@app.route("/account", methods=['GET', 'POST'])
def account():
    
    if not current_user.is_authenticated:
        return redirect(url_for('splash'))

    return render_template('account.html')

@app.route("/issues", methods=['GET', 'POST'])
def issues():
    
    if not current_user.is_authenticated:
        return redirect(url_for('splash'))

    return render_template('issues.html')

@app.route("/logout", methods=['GET'])
def logout():

    logout_user()
    return redirect(url_for('login'))
     

if __name__ == "__main__":
    app.run(debug=True)
