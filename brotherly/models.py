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

    def __repr__(self):
        return f"Contact('{self.first_name}', '{self.last_name}', '{self.image_file}')"
