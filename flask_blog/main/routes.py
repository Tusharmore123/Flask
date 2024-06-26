
from flask import Blueprint, render_template,request

from flask_blog.models import  Post

main=Blueprint('main',__name__)

@main.route("/")
@main.route("/home")
def home():
    page=request.args.get('page',1,type=int)
    posts=Post.query.order_by(Post.published_date.desc()).paginate(per_page=2,page=page)
    return render_template('home.html', Posts=posts)


@main.route("/about")
def about():
    return render_template('about.html', title='About')







