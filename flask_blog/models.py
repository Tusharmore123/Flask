from datetime import datetime
# from flask import db #it is in the situation called circcular imports
# since we import models in app.py
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer # type: ignore
# and then again we are importing db from app
from flask_blog import db,loginManger
from flask_login import UserMixin
from flask import current_app
# now flask in running with name __main__ so now we can access db and writing th import model
# after db

# but when we are using python shell and import db that time file name is app not __main__
# so we are again stuck
# so to avoid all these we create a package and then acess all the files 
@loginManger.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model,UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(120),unique=True,nullable=False)
    password=db.Column(db.String(20),nullable=False)
    email=db.Column(db.String,unique=True,nullable=False)
    image_file=db.Column(db.String(200),nullable=False,default='default.jpg')
    posts=db.relationship('Post',backref='author',lazy=True)
    def __repr__(self):
        return f"User ({self.name,self.email,self.image_file})"
    
    def get_reset_token(self,expire_sec):
        s=Serializer(current_app.config['SECRET_KEY'],expire_sec)
        token=s.dumps({'user_id':self.id}).decode('utf-8')
        return token
    
    def verify_token(token):
        s=Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id=s.loads(token)['user_id'] # type: ignore
        except:
            return None
        return User.query.get(user_id)

class Post(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(120),unique=True,nullable=False)
    content=db.Column(db.String(250),nullable=False)
    published_date=db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)

    def __repr__(self):
        return f"post ({self.title,self.published_date})"