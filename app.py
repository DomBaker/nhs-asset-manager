from flask import Flask, render_template, redirect, url_for
from flask_login import LoginManager, login_user, current_user, logout_user
import os

from forms import *
from models import *

#config app
app = Flask(__name__)
#needs some kind of security on this
app.secret_key = 'dom'
#hidden db URI stored directly in Heroku config vars - exported to local machine to run locally.
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URI")
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

@app.route("/account/", methods=['GET', 'POST'])
def account():

    update_form = UpdateForm()
    current_user = database.session.query(User).first()

    if update_form.validate_on_submit():
        email = update_form.email.data
        fname = update_form.fname.data
        lname = update_form.lname.data
        position = update_form.position.data
        password = update_form.password.data
        
        

    if not current_user.is_authenticated:
        return redirect(url_for('splash'))

    return render_template('account.html', form=update_form)

@app.route("/issues", methods=['GET', 'POST'])
def issues():
    
    if not current_user.is_authenticated:
        return redirect(url_for('splash'))

    return render_template('issues.html')

@app.route("/logout", methods=['GET'])
def logout():

    logout_user()
    return redirect(url_for('login'))

@app.route("/dashboard/current-assets", methods=['GET', 'POST'])
def current_assets():
    assets = Assets.query.all()

    return render_template('current-assets.html', assets=assets)

@app.route("/dashboard/all-assets", methods=['GET', 'POST'])
def all_assets():
    assets = Assets.query.all()

    return render_template('all-assets.html', assets=assets)


if __name__ == "__main__":
    app.run(debug=True)
