from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    SubmitField,
    BooleanField,
    SelectField,
    SelectMultipleField,
)
from wtforms.validators import DataRequired, Length, Email, EqualTo, Optional
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
        "Confirm Password",
        validators=[
            DataRequired(),
            EqualTo("password", message="Passwords must match!"),
        ],
    )
    submit = SubmitField(label="Register")


class searchForm(FlaskForm):
    # state = SelectField('Choose a state!', choices=['WA', 'OR', 'CA'], validators=[DataRequired()])
    state = SelectField(
        "Choose a State for Details", choices=STATE_LIST, validators=[DataRequired()]
    )
    submit = SubmitField(label="Search")


class SettingsForm(FlaskForm):
    """
    Form to change existing user settings.
    """

    email = StringField("Change email", validators=[Email(), DataRequired()])
    state = SelectField("Change state", choices=STATE_LIST, validators=[Optional()])
    new_password = PasswordField(
        label="Change password", validators=[Length(min=6, max=16), Optional()]
    )
    password = PasswordField(
        label="Re-enter current password to confirm updates",
        validators=[DataRequired(), Length(min=6, max=16)],
    )
    submit = SubmitField("Update")


class ActivitiesForm(FlaskForm):
    """
    Form to collect parameters for activities search.
    """

    # activs = SelectMultipleField("Activities", validators=[DataRequired()])
    activs = SelectMultipleField("Activities", validators=[Optional()])
    submit = SubmitField(label="Search")


# END
