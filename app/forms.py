from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")


class ServiceCallForm(FlaskForm):
    department = SelectField(
        "Department", choices=[("IT", "IT"), ("HR", "HR"), ("Finance", "Finance")]
    )
    urgency = SelectField(
        "Urgency",
        choices=[
            (">4 days", ">4 days"),
            ("<4 days", "<4 days"),
            ("<24 hours", "<24 hours"),
        ],
    )
    call_type = SelectField(
        "Call Type", choices=[("Issue", "Issue"), ("Request", "Request")]
    )
    description = TextAreaField(
        "Description", validators=[DataRequired(), Length(max=500)]
    )
    submit = SubmitField("Submit")


class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm = PasswordField("Confirm Password", validators=[DataRequired()])
    name = StringField("Name", validators=[DataRequired()])
    role = StringField("Role", validators=[DataRequired()])
    department = StringField("Department", validators=[DataRequired()])
    privilege = SelectField(
        "Privilege", choices=[(0, "No Privilege"), (1, "User"), (2, "Superuser")]
    )
    submit = SubmitField("Register")
