from flask import render_template, redirect, url_for, Blueprint
from flask_login import current_user

public = Blueprint('public', __name__)


@public.route("/")
@public.route("/welcome")
def welcome():
    if current_user.is_authenticated:
        return redirect(url_for('member.home'))
    else:
        return render_template('public/welcome.html', title="Welcome")
