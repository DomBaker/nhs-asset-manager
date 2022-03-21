from flask import Flask, render_template

from registration import *

#config app
app = Flask(__name__)
app.secret_key = 'dom'

@app.route("/", methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route("/register", methods=['GET', 'POST'])
def register():
    registration = RegForm()
    if registration.validate_on_submit():
        return render_template('success.html')
    return render_template('register.html', form=registration)

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


if __name__ == "__main__":
    app.run(debug=True)
