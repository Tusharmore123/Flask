
from datetime import datetime

from flask import Flask,render_template,flash,url_for,redirect # type: ignore
import os

from forms import RegisterForm,LoginForm
from flask_sqlalchemy import SQLAlchemy
# render template is used to render a particular code present in file mainly html
app=Flask(__name__,template_folder='../templates',static_folder='../static')

# secret key is required for csrf since wtf form includes its own csrf protection
app.config['SECRET_KEY']="47815d24cb6340f8cf2e"
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///site.db'
db=SQLAlchemy(app)
from models import User,Post


    



posts=[
    {
        'author':'tushar',
        'title':'Blog Post 1',
        'content':'Some text',
        'published_date':'28/05/2024'
    },
    {
        'author':'kunal',
        'title':'Blog Post 2',
        'content':'Some text',
        'published_date':'28/05/2024'
    }
]


@app.route('/')
def home():
    # return "<h1>Hello world</h1>"
    
    return render_template('home.html',Posts=posts)
# passing posts value to home.html
# we can access those values in post.html

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/register',methods=['GET','POST'])
def register():
    form=RegisterForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.name.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html',form=form,title="Register")

@app.route('/login',methods=['GET','POST'])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html',form=form,title="Login")
# command to run the flask server is flask run

if __name__=="__main__":
    
    app.debug=True#explicitly setting flask in debug mode
    # we can set the debug mode implicitly by setting the environment variable
    app.run()
