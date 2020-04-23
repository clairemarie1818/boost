from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flaskblog.models import User, Post


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])

    name = StringField('Name on Card', validators=[DataRequired()])
    creditcard = StringField('Credit Card Number', validators=[DataRequired()])
    expdate = StringField('Expiration Date', validators=[DataRequired()])
    cvc = StringField('CVC', validators=[DataRequired()])
    bill_address = StringField('Billing Address ', validators=[DataRequired()])
    bill_zip = StringField('Billing Zip Code', validators=[DataRequired()])

    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')


class PostForm(FlaskForm):
    title = StringField('Professional Title', validators=[DataRequired()])
    name = StringField("Name", validators = [DataRequired()])
    email = StringField("Email", validators = [DataRequired()])
    phone = StringField("Phone Number", validators = [DataRequired()])
    linkedin = StringField("LinkedIn URL")
    reference1_name = StringField("Reference 1 Name")
    reference1_number = StringField("Reference 1 Number/Email")
    reference2_name = StringField("Reference 2 Name")
    reference2_number = StringField("Reference 2 Number/Email")
    reference3_name = StringField("Reference 3 Name")
    reference3_number = StringField("Reference 3 Number/Email")
    portfolio = StringField("Portfolio URL")
    resume = FileField('Insert Resume', validators=[FileAllowed(['png', 'jpg'])])
    submit = SubmitField('Post')

class ProfProfile(FlaskForm):
    submit = SubmitField('Post')




