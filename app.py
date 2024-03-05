import os


from flask import Flask, render_template, redirect, session, flash
from models import connect_db, db, User
from forms import RegisterForm, LoginForm, CSRFProtectForm

app = Flask(__name__)

app.config['SECRET_KEY'] = "Secret"

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL", 'postgresql:///notes')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True


connect_db(app)

# change view function to homepage()
@app.get('/')
def redirect_to_register():
    """Redirects user to the register page"""

    return redirect('/register')

@app.route('/register', methods=["GET", "POST"])
def register_user():
    """Shows and handles the registration form"""

    form = RegisterForm()
# Remove error handling
    if form.validate_on_submit():
        user = User.register_user(
                username=form.username.data,
                password=form.password.data,
                email=form.email.data,
                first_name=form.first_name.data,
                last_name=form.last_name.data)
        if user:
            session["username"] = user.username

            return redirect(f"/users/{user.username}")
        else:
            flash("Username already exists.")
            return redirect('/')


    else:
        return render_template("registerForm.html", form = form)

@app.route('/login', methods=["GET", "POST"])
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

@app.get('/users/<username>')
def show_user_info(username):
    """Shows user information"""
    form = CSRFProtectForm()
    if "username" not in session:
        flash("You Must Be Logged In")
        return redirect('/')

    user = User.query.get_or_404(username)

    return render_template("user-profile.html", user=user, form =form)

@app.post("/logout")
def logout_user():
    """Handles current user loggout."""
    session.pop("username", None)
    return redirect('/')