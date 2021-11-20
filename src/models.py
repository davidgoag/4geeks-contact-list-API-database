from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     email = db.Column(db.String(120), unique=True, nullable=False)
#     password = db.Column(db.String(80), unique=False, nullable=False)
#     is_active = db.Column(db.Boolean(), unique=False, nullable=False)


class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(120), unique=False, nullable=False)
    address = db.Column(db.String(220), unique=False, nullable=True)
    phone = db.Column(db.String(220),unique=False, nullable=True) 
    email = db.Column(db.String(120), unique=True, nullable=True)


    def __repr__(self):
        return '<User %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "full_name": self.full_name,
            "adress": self.address,
            "phone": self.phone, 
            "email": self.email
            # do not serialize the password, its a security breach
        }