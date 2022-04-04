from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, login_user, current_user, logout_user
import os

from forms import *
from models import *

#config app
app = Flask(__name__)
#needs some kind of security on this
app.secret_key = os.environ.get('SECRET_KEY')
#hidden db URI stored directly in Heroku config vars - exported to local machine to run locally.
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE")
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

@app.route("/splash-out", methods=['GET', 'POST'])
def splashout():
    return render_template('splash-out.html')

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
        User.query.filter_by(email=email).first()
        user = User(email=email, fname=fname, lname=lname, position=position, password=secure_password)

        database.session.add(user)
        #commit the changes to the database
        database.session.commit()
        
        return redirect(url_for('login'))

    return render_template('register.html', form=registration)

@app.route("/login", methods=['GET', 'POST'])
def login():

    login_form = LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for('splashout'))

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

    update_form = UpdateForm()
    #Bit messy but works, could do with refactoring
    user_now = current_user.id
    update_user = database.session.query(User).filter_by(id=user_now).first()
    
    if request.method == 'POST' and update_form.validate_on_submit():
        update_user.fname = update_form.fname.data
        update_user.lname = update_form.lname.data
        update_user.position = update_form.position.data
        password = update_form.password.data
        
        update_user.password = pbkdf2_sha256.hash(password)

        #commit the changes to the database
        database.session.commit()

        flash('details updated successfully')

        return redirect(url_for('account'))
        

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
    flash('successfully logged out.')
    return redirect(url_for('login'))

@app.route("/dashboard/current-assets", methods=['GET', 'POST'])
def current_assets():
    form = UpdateCurrentAssets()

    #probably a better way of doing this by filtering out the current users id and comparing with owner_id instead of returning full table
    assets = Assets.query.all()

    #similar check to what is in the template, better to use backend logic for checks
    for asset in assets:
        if asset.owner_id == current_user.id:
            if request.method == 'POST' and form.validate_on_submit():
                asset.owner_id == None
                database.session.commit()
                flash('Successfully unassigned')

    return render_template('current-assets.html', assets=assets, form=form)

@app.route("/dashboard/all-assets", methods=['GET', 'POST'])
def all_assets():
    assets = Assets.query.all()

    return render_template('all-assets.html', assets=assets)


if __name__ == "__main__":
    app.run(debug=True)
