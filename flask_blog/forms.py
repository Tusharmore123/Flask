from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired,Length,Email,EqualTo,ValidationError
from flask_blog import db
from flask_wtf.file import FileField,FileAllowed
from flask_blog.models import User
from flask_login import current_user
class RegisterForm(FlaskForm):
    name=StringField('Name',validators=[DataRequired(),Length(min=5,max=15)])
    email=StringField('Email',validators=[DataRequired(),Email()])
    password=PasswordField('Password',validators=[DataRequired(),Length(min=8,max=15)])
    confirmPassword=PasswordField('ConfirmPassword',validators=[DataRequired(),EqualTo('password')])
    submit=SubmitField('Sign Up')

    def validate_name(self,name):
        userName=User.query.filter_by(name=name.data).first()
        if userName:
            raise ValidationError("User Already Exists")
        
    def validate_email(self,email):
        email=User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError("Email Already Exists")



class LoginForm(FlaskForm):
    email=StringField('Email',validators=[DataRequired(),Email()])
    password=PasswordField('Password',validators=[DataRequired(),Length(min=8,max=15)])
    submit=SubmitField('Login ')
    remember=BooleanField('Remember me')

class UpdateAccountForm(FlaskForm):
    name=StringField('Name',validators=[DataRequired(),Length(min=5,max=15)])
    email=StringField('Email',validators=[DataRequired(),Email()])
    picture=FileField('picture',validators=[FileAllowed(['jpg','png'])])
    submit=SubmitField('Update')

    def validate_name(self,name):
        if name.data!=current_user.name:
            user=User.query.filter_by(name=name.data).first()
            if user:
                raise ValidationError("User Already Exists")
        
    def validate_email(self,email):
        if email.data!=current_user.email:
            user=User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError("Email Already Exists")