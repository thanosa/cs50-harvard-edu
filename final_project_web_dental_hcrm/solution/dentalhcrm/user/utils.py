import os
from flask import url_for, current_app
from flask_mail import Message
from dentalhcrm import mail


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender='dev.test.geemail@gmail.com', recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('user.reset_token', token=token, _external=True)}

If you did not make this request then simple ignore this email and no changes will be made.
'''
    mail.send(msg)