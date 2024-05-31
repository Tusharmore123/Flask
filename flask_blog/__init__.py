
from datetime import datetime
from flask_login import LoginManager
from flask import Flask # type: ignore
import os
from flask_bcrypt import Bcrypt

from flask_sqlalchemy import SQLAlchemy
# render template is used to render a particular code present in file mainly html
app=Flask(__name__,template_folder='./templates',static_folder='./static')

# secret key is required for csrf since wtf form includes its own csrf protection
app.config['SECRET_KEY']="47815d24cb6340f8cf2e"
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///site.db'
db=SQLAlchemy(app)
bcrypt=Bcrypt(app)
loginManger=LoginManager(app)
loginManger.login_message_category='info'
LoginManager.login_view = 'login' # type: ignore
from flask_blog.models import User,Post
from flask_blog import routes

    


