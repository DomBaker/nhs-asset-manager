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

    registration = UserForm()

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

@app.route("/dashboard", methods=['GET'])
def dashboard():

    if not current_user.is_authenticated:
        return redirect(url_for('splash'))

    return render_template('dashboard.html')

@app.route("/account/<int:id>", methods=['GET', 'POST'])
def account(id):
    #instantiate a form & db query
    update_form = UserForm()
    user_to_update = database.session.query(User).get_or_404(id)

    if not current_user.is_authenticated:

        return redirect(url_for('splash'))

    elif request.method == 'GET':
        #pre-populate the form with the current user values
        update_form.email.data = current_user.email
        update_form.fname.data = current_user.fname
        update_form.lname.data = current_user.lname
        update_form.position.data = current_user.position

        return render_template('account.html', form=update_form, user_to_update=user_to_update)

    elif request.method == 'POST':
        user_to_update.email = request.form['email']
        user_to_update.fname = request.form['fname']
        user_to_update.lname = request.form['lname']
        user_to_update.position = request.form['position']
        password = request.form['password']

        user_to_update.password = pbkdf2_sha256.hash(password)

        try:
            database.session.commit()
            flash('User updated')
            return redirect(url_for('account', id=current_user.id))
        except:
            flash('User failed to update')
            return redirect(url_for('account'))
    else:
        return render_template('account.html', form=update_form, user_to_update=user_to_update)

@app.route("/account/delete", methods=['GET'])
def account_delete():
    update_form = UserForm()
    if not current_user.is_authenticated:
        return redirect(url_for('splash'))

    return render_template('delete-account.html', form=update_form) 
    

@app.route('/delete-account/<int:id>', methods=['GET','POST'])
def account_gone(id):
    form = UserForm()
    account_to_delete = database.session.query(User).get_or_404(id)

    try:
        database.session.delete(account_to_delete)
        database.session.commit()
        flash("User deleted")
        return render_template('login.html', form=form, account_to_delete=account_to_delete)
    except:
        flash("Unable to delete account right now, try again.")

@app.route('/delete-asset/<int:id>', methods=['GET','POST'])
def asset_gone(id):
    asset_to_delete = database.session.query(Assets).get_or_404(id)

    try:
        database.session.delete(asset_to_delete)
        database.session.commit()
        flash("Asset deleted")
        return render_template('all-assets.html', asset_to_delete=asset_to_delete)
    except:
        flash("Unable to delete asset as this time, try again.")

@app.route('/unassign/<int:id>', methods=['GET','POST'])
def asset_be_gone(id):
    asset_to_unassign = database.session.query(Assets).get_or_404(id)

    asset_to_unassign.owner_id = None

    try:
        database.session.commit()
        flash("Asset Un-assigned")
        return render_template('current-assets.html', asset_to_unassign=asset_to_unassign)
    except:
        flash("Unable to unassign asset as this time, try again.")

@app.route('/assign/<int:id>', methods=['GET','POST'])
def asset_be_assigned(id):
    asset_to_assign = database.session.query(Assets).get_or_404(id)

    asset_to_assign.owner_id = current_user.id

    try:
        database.session.commit()
        flash("Asset assigned successfully")
        return render_template('available-assets.html', asset_to_assign=asset_to_assign)
    except:
        flash("Unable to assign asset as this time, try again.")

@app.route("/logout", methods=['GET'])
def logout():

    logout_user()
    flash('successfully logged out')
    return redirect(url_for('login'))


@app.route("/dashboard/current-assets", methods=['GET', 'POST'])
def current_assets():
    
    assets = database.session.query(Assets).filter_by(owner_id=current_user.id).all()

    #similar check to what is in the template, better to use backend logic for checks
    if request.method == 'POST':
        assets.owner_id == None
        database.session.commit()
        flash('Successfully unassigned')

        return redirect(url_for('current_assets'))
        
    return render_template('current-assets.html', assets=assets)

@app.route("/dashboard/all-assets", methods=['GET'])
def all_assets():

    if current_user.is_admin and current_user.is_authenticated:
        assets = Assets.query.all()

    return render_template('all-assets.html', assets=assets)

@app.route("/dashboard/available-assets", methods=['GET'])
def available():

    if current_user.is_authenticated:
        assets = database.session.query(Assets).filter_by(owner_id=None).all()

    return render_template('available-assets.html', assets=assets)


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
            owner_id = form.owner_id.data
            asset_type = form.asset_type.data
            serial_number = form.serial_number.data 

            some_serial = Assets.query.filter_by(serial_number=serial_number).first()
            if some_serial == serial_number:
                flash('Serial number already assigned to asset')
            asset = Assets(asset_name=asset_name, owner_id=owner_id, asset_type=asset_type, serial_number=serial_number)

            database.session.add(asset)
            database.session.commit()
            flash("Asset successfully added")
            return redirect(url_for('admin_assets'))  
    else:
        return redirect(url_for('splashout'))

    return render_template('admin-assets.html', form=form)


if __name__ == "__main__":
    app.run(debug=True)
