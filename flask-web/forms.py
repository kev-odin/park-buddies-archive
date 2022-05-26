from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from app_lists import STATE_LIST


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
    state = SelectField("Select state", choices=STATE_LIST, validators=[DataRequired()])
    password = PasswordField(
        "Enter password", validators=[DataRequired(), Length(min=6, max=16)]
    )
    password2 = PasswordField(
        "Confirm Password", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField(label="Register")


class SettingsForm(FlaskForm):
    """
    Form to change existing user settings.
    """

    old_password = PasswordField(
        label="Current Password", validators=[DataRequired(), Length(min=6, max=16)]
    )
    new_password = PasswordField(
        label="New Password", validators=[DataRequired(), Length(min=6, max=16)]
    )
    verify_password = PasswordField(
        label="Confirm Password", validators=[DataRequired(), Length(min=6, max=16)]
    )

    submit = SubmitField("Change Password")
