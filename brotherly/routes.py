from flask import render_template, url_for, flash, redirect, request, abort
from brotherly import app, db, bcrypt
from brotherly.forms import ResgistrationForm, LoginForm, ContactForm, ReminderForm
from brotherly.models import User, Contacts, Reminder
from flask_login import login_user, current_user, logout_user , login_required
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
            return redirect(next_page) if next_page else redirect(url_for('contacts'))
        else:
            flash("Login unsuccessful! Please check email or password", 'danger')
    return render_template('sign_in.html', title='Sign In', form=form)

@app.route("/contacts", strict_slashes=False)
@login_required
def contacts():
    contacts = Contacts.query.filter_by(user_id=current_user.id).all()
    return render_template('contacts.html', title='Contacts', contacts=contacts)

@app.route("/add_contact", methods=['GET', 'POST'], strict_slashes=False)
@login_required
def add_contact():
    form = ContactForm()
    if form.validate_on_submit():
        contact = Contacts(
            first_name=form.first_name.data, last_name=form.last_name.data,
            phone=form.phone.data, birthday=form.birthday.data,
            interests=form.interests.data, user=current_user
        )
        db.session.add(contact)
        db.session.commit()
        return redirect(url_for('contacts'))
    return render_template('add_contact.html', title='Add Contact', form=form)


@app.route("/reminders", strict_slashes=False)
@login_required
def reminders():
    # contacts = Contacts.query.filter_by(user_id=current_user.id).all()
    return render_template('reminders.html', title='Reminders')


@app.route('/add_reminder', methods=['GET', 'POST'], strict_slashes=False)
@login_required
def add_reminder():
    form = ReminderForm()
    
    # Assuming you have a way to get the current user's contacts
    user_contacts = Contacts.query.filter_by(user_id=current_user.id).all()
    
    # Populate form with contact choices (e.g., contact ID and name)
    form.contact.choices = [(contact.id, contact.first_name+''+contact.last_name) for contact in user_contacts]
    
    if form.validate_on_submit():
        # Handle the form submission and save the reminder
        pass
    
    return render_template('add_reminder.html', title='Add Reminder', form=form)


@app.route("/sign_out")
def sign_out():
    logout_user()
    return redirect(url_for('home'))
