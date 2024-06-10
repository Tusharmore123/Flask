

from flask import  render_template, url_for, flash, redirect, request,Blueprint
from flask_blog import  db, bcrypt
from flask_blog.Users.forms import RegisterForm, LoginForm, UpdateAccountForm,ResetForm,ResetPassword
from flask_blog.models import User
from flask_login import login_user, current_user, logout_user, login_required
import os
from flask_blog.Users.utils import save_picture,send_mail


users=Blueprint('users',__name__)


@users.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(name=form.name.data, email=form.email.data, password=hashed_password) # type: ignore
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)


@users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))






    


@users.route('/reset_password',methods=['GET','POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form=ResetForm()
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        send_mail(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('users.login'))
        
    return render_template('reset.html',title='Reset Email',form=form)

@users.route('/reset_password/<token>',methods=['GET','POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPassword()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('users.login'))
    return render_template('resetPassword.html', title='Reset Password', form=form)

@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            picture_file=os.path.splitext(picture_file)
            current_user.image_file = picture_file
        current_user.name = form.name.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.name.data = current_user.name
        form.email.data = current_user.email
    image_file = url_for('static', filename= current_user.image_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)