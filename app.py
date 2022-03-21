from flask import Flask, render_template

from registration import *

#config app
app = Flask(__name__)
app.secret_key = 'dom'

@app.route("/", methods=['GET', 'POST'])
def index():
    registration = RegForm()
    if registration.validate_on_submit():
        return "great success"
    return render_template('index.html', form=registration)


if __name__ == "__main__":
    app.run(debug=True)
