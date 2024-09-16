from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, DateField, SelectField, DateTimeField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from brotherly.models import User
"""
from flask_wtf.file import FileField, FileAllowed
from flask_blog_package import bcrypt
from flask_login import current_user
"""
class ResgistrationForm(FlaskForm):
    first_name = StringField(
        'First name', validators=[DataRequired(), Length(min=2, max=20)]
        )
    last_name = StringField(
        'Last name', validators=[DataRequired(), Length(min=2, max=20)]
        )
    email = StringField(
        'Email', validators=[DataRequired(), Email()]
        )
    password = PasswordField(
        'Password', validators=[DataRequired()]
        )
    confirm_password = PasswordField(
        'Confirm Password', validators=[DataRequired(), EqualTo('password')]
        )
    submit = SubmitField('Sign Up')
        
    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError("Email already exists! Please use a different one")


class LoginForm(FlaskForm):
    email = StringField(
        'Email', validators=[DataRequired(), Email()]
        )
    password = PasswordField(
        'Password', validators=[DataRequired()]
        )
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class ContactForm(FlaskForm):
    first_name = StringField('First name', validators=[DataRequired()])
    last_name = StringField('Last name', validators=[DataRequired()])
    phone = StringField('Phone')
    birthday = DateField('Birthday', format='%Y-%m-%d')
    interests = TextAreaField('Interests')
    submit = SubmitField('Add')


class ReminderForm(FlaskForm):
    due_date = DateTimeField(
        'Due date and time', 
        format='%Y-%m-%d %H:%M',  # Date and time format (24-hour format)
        validators=[DataRequired()]
    )
    frequency = SelectField(
        'Frequency',
        choices=[('one-off', 'One-Off'), ('daily', 'Daily'), ('weekly', 'Weekly'), ('monthly', 'Monthly')],
        validators=[DataRequired()]
    )
    message = TextAreaField('Reminder message')
    contact = SelectField('Contact', validators=[DataRequired()])
    submit = SubmitField('Add')


"""
class UpdateProfileForm(FlaskForm):
    username = StringField(
        'Username', validators=[DataRequired(), Length(min=2, max=20)]
        )
    email = StringField(
        'Email', validators=[DataRequired(), Email()]
        )
    picture = FileField('Update profile picture', validators=[FileAllowed(['jpg', 'jpeg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError("Username already exists! Please choose a different one")
        
    def validate_email(self, email):
        if email.data != current_user.email:
            email = User.query.filter_by(email=email.data).first()
            if email:
                raise ValidationError("Email already exists! Please use a different one")
"""