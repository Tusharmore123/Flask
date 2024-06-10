

from flask_login import LoginManager
from flask import Flask # type: ignore

from flask_bcrypt import Bcrypt
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
# render template is used to render a particular code present in file mainly html

db=SQLAlchemy()
bcrypt=Bcrypt()
loginManger=LoginManager()
# type: ignore
loginManger.login_message_category='info'
LoginManager.login_view = 'user.login'  # type: ignore
mail=Mail()


    
def create_app():
    app=Flask(__name__,template_folder='./templates',static_folder='./static')

    # secret key is required for csrf since wtf form includes its own csrf protection
    app.config['SECRET_KEY']="47815d24cb6340f8cf2e"
    app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///site.db'
    app.config['MAIL_SERVER']='smtp.gmail.com'
    app.config['MAIL_PORT']=587
    app.config['MAIL_USE_TLS']=True
    app.config['MAIL_USE_SSL'] = False
    app.config['MAIL_USERNAME']='tusharmore160102@gmail.com'
    app.config['MAIL_PASSWORD']='hnun mkus opiv dfzd'
    from flask_blog.models import User,Post
    from flask_blog.Users.routes import users
    from flask_blog.Posts.routes import posts
    from flask_blog.main.routes import main 
    from flask_blog.Errors.handlers import errors
    db.init_app(app)
    bcrypt.init_app(app)
    loginManger.init_app(app) # type: ignore
    
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)
    return app
