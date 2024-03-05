import os

from flask import Flask, render_template, redirect, session, flash
from models import connect_db, db, User
from forms import RegisterForm, LoginForm

app = Flask(__name__)

app.config['SECRET_KEY'] = "Secret"

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL", 'postgresql:///notes')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True


connect_db(app)


@app.get('/')
def redirect_to_register():
    """Redirects user to the register page"""

    return redirect('/register')

@app.route('/register', methods=["GET", "POST"])
def register_user():
    """Shows and handles the registration form"""

    form = RegisterForm()

    if form.validate_on_submit():
        try:
            user = User.register_user(
                username=form.username.data,
                password=form.password.data,
                email=form.email.data,
                first_name=form.first_name.data,
                last_name=form.last_name.data
            )
        except:
            return redirect('/register')

        db.session.add(user)
        db.session.commit()
        session["username"] = user.username

        return redirect(f"/users/{user.username}")
    else:
        return render_template("registerForm.html")

app.route('/login', methods=["GET", "POST"])
def login_user():
    """Shows and handles login form"""

    form = LoginForm()

    if form.validate_on_submit():
        user = User.validate_user(
            username=form.username.data,
            password=form.password.data)

        if user:
            session["username"] = user.username
            return redirect(f"/users/{user.username}")

        else:
            flash("incorrect username/password")
            return render_template('loginForm.html', form=form)

    else:
        return render_template('loginForm.html', form=form)