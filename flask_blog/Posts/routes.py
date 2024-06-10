from flask import  Blueprint, render_template, url_for, flash, redirect, request,abort
from flask_blog import db, bcrypt,mail
from flask_blog.Posts.form import PostForm # type: ignore
from flask_blog.models import Post
from flask_login import current_user, login_required


posts=Blueprint('posts',__name__)


@posts.route('/new_posts',methods=['GET','POST'])
@login_required
def new():
    form=PostForm()
    if form.validate_on_submit():
        posts=Post(title=form.title.data,content=form.content.data,author=current_user) # type: ignore
        db.session.add(posts)
        db.session.commit()
        return redirect(url_for('main.home'))
    return render_template('create_post.html',title='New Post',form=form)



@posts.route('/post/<int:post_id>')
def post(post_id):
    post=Post.query.get_or_404(post_id)
    return render_template('post.html',title=f"Post {post_id}",post=post)


@posts.route('/post/<int:post_id>/update',methods=['GET','POST'])
@login_required
def update_post(post_id):
    post=Post.query.get_or_404(post_id)
    form=PostForm()
    if post.author!=current_user:
        abort(403)
    if form.validate_on_submit():
        post.title=form.title.data
        post.content=form.content.data
        db.session.commit()
        redirect(url_for('main.home'))
    elif request.method=="GET":
        form.title.data=post.title
        form.content.data=post.content
    return render_template('create_post.html',title='Update Post',form=form)


@posts.route('/delete/<int:post_id>',methods=['GET',"POST"])
def delete_post(post_id):
    post=Post.query.get_or_404(post_id)
    if post.author!=current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Deleted Post Successfully','info')
    return redirect(url_for('main.home'))

