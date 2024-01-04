from main import db, app

class Users(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(40))

    def __init__(self, name, email):
        self.name = name
        self.email = email