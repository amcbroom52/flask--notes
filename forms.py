from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import InputRequired, Email


class RegisterForm(FlaskForm):
    """Form for registering new user"""

    username = StringField(
        "Username",
        validators=[InputRequired()]
    )

    password = PasswordField(
        "Password",
        validators=[InputRequired()]
    )

    email = StringField(
        "Email",
        validators=[
            InputRequired(),
            Email()
        ]
    )

    first_name = StringField(
        "First Name",
        validators=[InputRequired()]
    )

    last_name = StringField(
        "Last Name",
        validators=[InputRequired()]
    )

class LoginForm(FlaskForm):
    """Form for logging in user"""

    username = StringField(
        "Username",
        validators=[InputRequired()]
    )

    password = PasswordField(
        "Password",
        validators=[InputRequired()]
    )

class AddNoteForm(FlaskForm):
    """Form for adding a new note"""

    title = StringField(
        "Title",
        validators=[InputRequired()]
    )

    content = TextAreaField(
        'Content',
        validators=[InputRequired()]
    )

class EditNoteForm(FlaskForm):
    """Form for editing a note"""

    title = StringField(
        "Title",
        validators=[InputRequired()]
    )

    content = TextAreaField(
        'Content',
        validators=[InputRequired()]
    )


class CSRFProtectForm(FlaskForm):
    """For just for CSRF Protection"""