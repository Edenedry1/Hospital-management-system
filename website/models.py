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





