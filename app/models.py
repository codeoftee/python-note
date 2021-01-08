from datetime import datetime

from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    phone = db.Column(db.String(15))
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(200))
    registered = db.Column(db.DateTime(), default=datetime.utcnow())

    def __repr__(self):
        return '<User {}>'.format(self.name)
