from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, login_user, current_user, logout_user
import os

from forms import *
from models import *

#With increasing complexity this file could be broken down into it's core sections, I haven't done this as the application is lightweight and unnecessary modularity can prove confusing.

# App config and db setup ---------------------------------------------------------------------------------------

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

#ROUTES ---------------------------------------------------------------------------------------------------------

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

@app.route("/admin-splash", methods=['GET', 'POST'])
def admin_splash():
    return render_template('admin-splash.html')

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

        #have to convert this to bool as return type of SelectField is a string
        update_user.is_admin = bool(update_form.is_admin.data)
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

@app.route("/logout", methods=['GET'])
def logout():

    logout_user()
    flash('successfully logged out.')
    return redirect(url_for('login'))

@app.route("/dashboard/current-assets", methods=['GET', 'POST'])
def current_assets():
    form = UpdateCurrentAssets()

    #probably a better way of doing this by filtering out the current users id and comparing with owner_id instead of returning full table
    assets = database.session.query(Assets).filter_by(owner_id=current_user.id).all()

    #similar check to what is in the template, better to use backend logic for checks
    if request.method == 'POST' and form.validate_on_submit():
        assets.owner_id == None
        database.session.commit()
        flash('Successfully unassigned')

        return redirect(url_for('current_assets'))
        
    return render_template('current-assets.html', assets=assets, form=form)

@app.route("/dashboard/all-assets", methods=['GET'])
def all_assets():

    if current_user.is_admin and current_user.is_authenticated:
        assets = Assets.query.all()

    return render_template('all-assets.html', assets=assets)


@app.route("/admin-view-all-users", methods=['GET', 'POST'])
def admin_view_all_users():
    if current_user.is_admin and current_user.is_authenticated:
        all_users = User.query.all()
        return render_template('admin-view-users.html', all_users=all_users)
    else:
        return redirect(url_for('admin_splash'))

@app.route("/dashboard/admin-assets", methods=['GET', 'POST'])
def admin_assets():
    form = AddAsset()

    if current_user.is_admin:
        if form.validate_on_submit():
            asset_name = form.asset_name.data
            asset_type = form.asset_type.data
            serial_number = form.serial_number.data 

            some_serial =Assets.query.filter_by(serial_number=serial_number).first()
            if some_serial == serial_number:
                flash('Serial number already assigned to asset')
            asset = Assets(asset_name=asset_name, asset_type=asset_type, serial_number=serial_number)

            database.session.add(asset)
            database.session.commit()
            flash("Asset successfully added")
            return redirect(url_for('admin_assets'))  
    else:
        return redirect(url_for('splashout'))

    return render_template('admin-assets.html', form=form)

if __name__ == "__main__":
    app.run(debug=True)
