from datetime import datetime
from flaskblog import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)

    name = db.Column(db.String(20), unique=True, nullable=True)
    creditcard = db.Column(db.String(20), unique=True, nullable=True)
    expdate = db.Column(db.String(4), unique=True, nullable=True)
    cvc = db.Column(db.String(4), unique=True, nullable=True)
    bill_address = db.Column(db.String(40), unique=True, nullable=True)
    bill_zip = db.Column(db.String(6), unique=True, nullable=True)

    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) 
    resume = db.Column(db.String(20), nullable=True, default='default.jpg')
    name = db.Column(db.String(100), nullable=True)
    email = db.Column(db.String(100), nullable=True)
    phone = db.Column(db.String(100), nullable=True)
    linkedin = db.Column(db.String(100), nullable=True)
    reference1_name = db.Column(db.String(100), nullable=True)
    reference1_number = db.Column(db.String(100), nullable=True)
    reference2_name = db.Column(db.String(100), nullable=True)
    reference2_number = db.Column(db.String(100), nullable=True)
    reference3_name = db.Column(db.String(100), nullable=True)
    reference3_number = db.Column(db.String(100), nullable=True)
    portfolio = db.Column(db.String(100), nullable=True)


    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"
