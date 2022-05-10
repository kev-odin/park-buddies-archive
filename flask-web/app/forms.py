from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class LoginForm(FlaskForm):
    """
    Form to collect existing user credentials. 
    """
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField(
        label="Password", validators=[DataRequired(), Length(min=6, max=16)]
    )
    remember = BooleanField("Remember Me")
    submit = SubmitField("Login")


class RegisterForm(FlaskForm):
    """
    Form to collect new user information that will be added to the database.
    """
    email = StringField("Enter email", validators=[DataRequired(), Email()])
    password_one = PasswordField(
        "Enter password", validators=[DataRequired(), Length(min=6, max=16)]
    )
    password_two = PasswordField(
        "Re-enter password", validators=[DataRequired(), EqualTo(password_one)]
    )
    submit = SubmitField(label="Register")
