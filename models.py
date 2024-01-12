from .main import db, app
from flask_login import UserMixin


class User(db.Model, UserMixin):
    id = db.Column("id", db.Integer, primary_key=True)
    username = db.Column("username", db.String(100), unique=True, nullable=False)
    email = db.Column("email", db.String(80), unique=True, nullable=False)
    password = db.Column("password", db.String(24), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username
