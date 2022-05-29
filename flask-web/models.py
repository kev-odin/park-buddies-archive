from hashlib import md5
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, LoginManager

db = SQLAlchemy()
login = LoginManager()


class UserModel(UserMixin, db.Model):
    """
    Base ORM table to be used with SQLAlchemy
    """

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    state = db.Column(db.String(2), unique=False, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(), nullable=False)

    def set_password(self, password):
        """
        Security measure to ensure no passwords are hard coded within the application.
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """
        Security measuer to validate passwords within a database.
        """
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode("utf-8")).hexdigest()
        return f"https://www.gravatar.com/avatar/{digest}?d=robohash&s={size}"

    def __repr__(self):
        return f"{self.id} | {self.state} | {self.email}"


@login.user_loader
def load_user(id):
    return UserModel.query.get(int(id))
