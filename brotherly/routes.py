from flask import render_template, url_for, flash, redirect, request #, abort
from brotherly import app, db, bcrypt
from brotherly.forms import ResgistrationForm, LoginForm
from brotherly.models import User
from flask_login import login_user, current_user, logout_user #, login_required
"""
import os
from PIL import Image
"""


@app.route("/")
@app.route("/home", strict_slashes=False)
def home():
    features = [
        {
            'title': "Reminder Notifications",
            'description': "Set up reminders to check in with your contacts regularly and never miss an important occasion."
        },
        {
            'title': "Event Tracker",
            'description': "Keep track of birthdays, anniversaries, and other special occasions to show you care."
        },
        {
            'title': "Gesture Suggestions",
            'description': "Receive suggestions for kind gestures and thoughtful messages to strengthen your relationships."
        }
    ]
    return render_template('home.html', features=features)

@app.route("/register", methods=['GET', 'POST'], strict_slashes=False)
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = ResgistrationForm()
    if form.validate_on_submit():
        hashed_pword = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(
            first_name=form.first_name.data, last_name=form.last_name.data,
            username=f"{form.first_name.data} {form.last_name.data}", email=form.email.data,
            password=hashed_pword
            )
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('sign_in'))
    return render_template('register.html', title='Register', form=form)

@app.route("/sign_in", methods=['GET', 'POST'], strict_slashes=False)
def sign_in():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash(f'You have been logged in!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash("Login unsuccessful! Please check email or password", 'danger')
    return render_template('sign_in.html', title='Sign In', form=form)

@app.route("/contacts", strict_slashes=False)
def contacts():
    return render_template('contacts.html', title='Contacts')

@app.route("/sign_out")
def sign_out():
    logout_user()
    return redirect(url_for('home'))
