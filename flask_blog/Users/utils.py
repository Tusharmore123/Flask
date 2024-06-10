import os
import secrets

from flask import  url_for,current_app


from flask_blog import mail
from flask_mail import Message



def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static', picture_fn)

    form_picture.save(picture_path)

    return picture_fn

def send_mail(user):
    token=user.get_reset_token(18000)
    msg=Message('Password request reset',
                sender='tusharmore160102@gmail.com',
                recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('reset_token', token=token, _external=True)}

If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)  

