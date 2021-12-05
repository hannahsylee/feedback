from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField
from wtforms.validators import InputRequired, Length

class UserForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired(message="Username must be filled"), Length(max=20, message="Username is longer than 20 characters")])
    password = PasswordField("Password", validators=[InputRequired(message="Password must be filled")])
    email = EmailField("Email", validators=[InputRequired("Email must be filled"), Length(max=50, message="Email is longer than 50 characters")])
    first_name = StringField("First Name", validators=[InputRequired("First name must be filled"), Length(max=30, message="First name is longer than 30 characters")])
    last_name = StringField("Last Name", validators = [InputRequired("Last name must be filled"), Length(max=30, message="Last name is longer than 30 characters")])

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired(message="Username must be filled")])
    password = PasswordField("Password", validators=[InputRequired(message="Password must be filled")])

class FeedbackForm(FlaskForm):
    title = StringField("Title", validators=[InputRequired(message="Title required"), Length(max=100, message="Title is longer than 100 characters")])
    content = StringField("Content", validators=[InputRequired(message="Content required")])

class DeleteForm(FlaskForm):
    """Delete form -- this form is intentionally blank."""



