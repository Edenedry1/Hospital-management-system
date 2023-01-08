from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
'''
#create database models
'''

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ID = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    # user_ID = db.Column(db.Integer, db.ForeignKey('user.ID'))


class User(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    Name = db.Column(db.String(150))
    role = db.Column(db.String(150))
    is_active_patient = db.Column(db.Integer)
    allergy = db.Column(db.String(150))
    n_action = db.Column(db.String(30))
    answer = db.Column(db.String(30))
    reason = db.Column(db.String(200))
    place_in_queue = db.Column(db.Integer)
    s_action = db.Column(db.String(20))
    is_approved = db.Column(db.Integer)
    message = db.Column(db.String(200))

class Chat(db.Model):
    message_id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer)
    content = db.Column(db.String(200))





