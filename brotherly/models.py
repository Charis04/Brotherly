from datetime import datetime
from brotherly import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False,  default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    contacts = db.relationship('Contacts', backref='user', lazy=True)
    reminders = db.relationship('Reminder', backref='user', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Contacts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    phone = db.Column(db.String(20), unique=True)
    birthday = db.Column(db.DateTime)
    interests = db.Column(db.Text)
    image_file = db.Column(db.String(20), nullable=False,  default='default.jpg')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, )
    reminders = db.relationship('Reminder', backref='contact', lazy=True)

    def __repr__(self):
        return f"Contact('{self.first_name}', '{self.last_name}', '{self.image_file}')"


class Reminder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, index=True)
    contact_id = db.Column(db.Integer, db.ForeignKey('contacts.id'), nullable=True, index=True)
    frequency = db.Column(db.String(10), nullable=False) # one-off, daily, weekly, or monthly
    due_date = db.Column(db.DateTime)
    message = db.Column(db.Text, default='This is a reminder message')
    done = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"Reminder('{self.due_date}', '{self.frequency}', '{self.done}')"
