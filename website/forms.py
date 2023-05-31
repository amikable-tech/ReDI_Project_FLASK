from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateField, TimeField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from datetime import datetime


class SignupForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Log In')


class AppointmentForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired(), Length(max=50)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(max=50)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    date = DateField('Date', validators=[DataRequired()])
    time = TimeField('Time', validators=[DataRequired()])
    message = TextAreaField('Message', validators=[Length(max=200)])
    submit = SubmitField('Book Appointment')

    @staticmethod
    def validate_date(field):
        if field.data < datetime.now().date():
            raise ValidationError('Invalid date. Please choose a future date.')

    def validate_time(self, field):
        now = datetime.now().time()
        if self.date.data == datetime.now().date() and field.data <= now:
            raise ValidationError('Invalid time. Please choose a future time.')
