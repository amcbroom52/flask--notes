from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from sqlalchemy.exc import IntegrityError

db = SQLAlchemy()
bcrypt = Bcrypt()

def connect_db(app):
    """Connect this database to provided Flask app. Called in app.py"""

    app.app_context().push()
    db.app = app
    db.init_app(app)

class User(db.Model):
    """User Model"""

    __tablename__ = "users"
# put class methods below properties
    @classmethod
    def register_user(cls, username, password, email, first_name, last_name):
        """Checks registration of a new user"""

        hash = bcrypt.generate_password_hash(password).decode("utf8")
        try:
            user =  cls(
                username=username,
                hashed_password=hash,
                email=email,
                first_name=first_name,
                last_name=last_name
            )
            ##.commit needs to go in app.py
            db.session.add(user)
            db.session.commit()
            return user
        except IntegrityError:
            return False

    @classmethod
    # change function to authenticate
    def validate_user(cls, username, password):
        """Authenticate user"""

        user = cls.query.filter_by(username=username).one_or_none()

        if user and bcrypt.check_password_hash(user.hashed_password, password):
            return user
        else:
            return False


    username = db.Column(
        db.String(20),
        primary_key=True
    )

    hashed_password = db.Column(
        db.String(100),
        nullable=False
    )
# make email unique (don't forget to drop the table)
    email = db.Column(
        db.String(50),
        nullable=False
    )

    first_name = db.Column(
        db.String(30),
        nullable=False
    )

    last_name = db.Column(
        db.String(30),
        nullable=False
    )