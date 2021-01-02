from flask import render_template, url_for, flash, redirect, request, Blueprint, session
from flask_login import login_user, logout_user, current_user, login_required
from dentalhcrm import db, bcrypt
from dentalhcrm.user.forms import (RegistrationForm, LoginForm, 
                             RequestResetForm, ResetPasswordForm, 
                             UpdateAccountInfoForm, UpdatePasswordForm)
from dentalhcrm.user.models import User
from dentalhcrm.user.utils import send_reset_email

user = Blueprint('user', __name__)


@user.route("/signup", methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('public.welcome'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        # The user is create with the email as the initial username
        user = User(username=form.email.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account has been created!', 'success')
        return redirect(url_for('user.login'))
    return render_template('user/signup.html', title="Signup", form=form)


@user.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('public.welcome'))

    MAX_ATTEMPTS = 3
    attempts = session['login_attempts'] = session.get('login_attempts', 0) + 1
    if attempts >= MAX_ATTEMPTS:
        flash(f'Maximum login attempts reached. Please request a password reset', 'danger')
        return redirect(url_for('user.reset_request'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            session['login_attempts'] = 0
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('public.welcome'))
        else:
            flash(f'Login Failed. {MAX_ATTEMPTS - attempts} attempt(s) remaining', 'warning')
    return render_template('user/login.html', title="Login", form=form)


@user.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('public.welcome'))


@user.route("/update_password", methods=['GET', 'POST'])
@login_required
def update_password():
    form = UpdatePasswordForm()
    form.email.data = current_user.email
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.current_password.data):
            hashed_password = bcrypt.generate_password_hash(form.new_password.data).decode('utf-8')
            user.password = hashed_password
            db.session.commit()
            session['login_attempts'] = 0
            flash(f'Your password has been changed!', 'success')
            return redirect(url_for('user.account'))
        else:
            flash(f'Current password is incorrect', 'danger')
    return render_template('user/update_password.html', title="Update Password", form=form)


@user.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('public.welcome'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password', 'info')
        return redirect(url_for('user.login'))
    return render_template('user/reset_request.html', title="Reset Password", form=form)


@user.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('public.welcome'))

    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token.', 'warning')
        return redirect(url_for('user.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        session['login_attempts'] = 0
        flash(f'Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('user.login'))
    return render_template('user/reset_token.html', title="Reset Password", form=form)


@user.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountInfoForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        # not sure if next line is needed
        # # return redirect(url_for('user.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template('user/account.html', title="Account", form=form)
