from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired,Length,Email,EqualTo

class RegisterForm(FlaskForm):
    name=StringField('Name',validators=[DataRequired(),Length(min=5,max=15)])
    email=StringField('Email',validators=[DataRequired(),Email()])
    password=PasswordField('Password',validators=[DataRequired(),Length(min=8,max=15)])
    confirmPassword=PasswordField('ConfirmPassword',validators=[DataRequired(),EqualTo('password')])
    submit=SubmitField('Sign Up')

class LoginForm(FlaskForm):
    email=StringField('Email',validators=[DataRequired(),Email()])
    password=PasswordField('Password',validators=[DataRequired(),Length(min=8,max=15)])
    submit=SubmitField('Login ')
    remember=BooleanField('Remember me')
