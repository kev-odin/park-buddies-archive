from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
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
    password = PasswordField(
        "Enter password",
        validators=[
            DataRequired(),
            Length(min=6, max=16),
        ],
    )
    submit = SubmitField(label="Register")

class searchForm(FlaskForm):
    state = SelectField('Choose a state!', validators=DataRequired(), choices=[('Washington', 'WA'), ('Oregon', 'OR'), ('California', 'CA')])
    submit = SubmitField("Search")