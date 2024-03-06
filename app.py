import os


from flask import Flask, render_template, redirect, session, flash
from models import connect_db, db, User, Note
from forms import RegisterForm, LoginForm, CSRFProtectForm, AddNoteForm, EditNoteForm

SESSION_USER_KEY = "username"

app = Flask(__name__)

app.config['SECRET_KEY'] = "Secret"

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL", 'postgresql:///notes')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True


connect_db(app)


@app.get('/')
def homepage():
    """Redirects user to the register page"""

    return redirect('/register')

@app.route('/register', methods=["GET", "POST"])
def register_user():
    """Shows and handles the registration form"""

    form = RegisterForm()

    if form.validate_on_submit():
        user = User.register_user(
            username=form.username.data,
            password=form.password.data,
            email=form.email.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data
        )

        db.session.add(user)
        db.session.commit()
        session[SESSION_USER_KEY] = user.username

        return redirect(f"/users/{user.username}")

    else:
        return render_template("registerForm.html", form = form)

@app.route('/login', methods=["GET", "POST"])
def login_user():
    """Shows and handles login form"""

    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate_user(
            username=form.username.data,
            password=form.password.data)

        if user:
            session[SESSION_USER_KEY] = user.username
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

    if SESSION_USER_KEY not in session:
        flash("You Must Be Logged In")
        return redirect('/')

    if session[SESSION_USER_KEY] != username:
        flash("Cannot access page of other users")
        return redirect(f"/users/{session[SESSION_USER_KEY]}")

    user = User.query.get_or_404(username)

    return render_template("user-profile.html", user=user, form =form)

@app.post("/logout")
def logout_user():
    """Handles current user logout."""


    form = CSRFProtectForm()

    if form.validate_on_submit():
        session.pop(SESSION_USER_KEY, None)
        return redirect('/')


############################ Part 2 ################################


@app.post('/users/<username>/delete')
def delete_user(username):
    """Deletes user from DB"""

    if session.get(SESSION_USER_KEY) != username:
        flash ("Must be logged into delete and can only delete own user!")
        return redirect('/')

    ##Check valid submit

    user = User.query.get_or_404(username)

    Note.query.filter_by(owner_username = username).delete()
    db.session.delete(user)
    db.session.commit()

    session.pop(SESSION_USER_KEY, None)

    return redirect('/')



@app.route('/users/<username>/notes/add', methods=["GET", "POST"])
def add_note(username):
    """Shows and handles add note form"""

    if session.get(SESSION_USER_KEY) != username:
        flash ("Must be logged in to add note!")
        return redirect('/')

    form = AddNoteForm()

    if form.validate_on_submit():
        note = Note(
            title=form.title.data,
            content=form.content.data,
            owner_username=username
        )

        db.session.add(note)
        db.session.commit()

        return redirect(f'/users/{username}')

    else:
        return render_template('addNotePage.html', form=form)

@app.route('/notes/<int:note_id>/update', methods=["GET","POST"])
def update_note(note_id):
    """Updates Note"""

    note = Note.query.get_or_404(note_id)
    form = EditNoteForm(obj = note)

    if session.get(SESSION_USER_KEY) != note.owner_username:
        flash ("Must be logged in and note must be yours")
        return redirect('/')


    if form.validate_on_submit():
        note.title = form.title.data
        note.content = form.content.data


        db.session.commit()

        return redirect(f'/users/{note.owner_username}')




    return render_template("editNotePage.html", form = form, note = note)

@app.post("/notes/<int:note_id>/delete")
def delete_note(note_id):
    """Deletes note"""

    note = Note.query.get_or_404(note_id)
    username = note.owner_username

    if session.get(SESSION_USER_KEY) != username:
        flash ("Must be logged in and note must be yours")
        return redirect('/')

    db.session.delete(note)
    db.session.commit()

    return redirect(f"/users/{username}")