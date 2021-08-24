from enum import unique
from app import db
from app import login
import enum

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class EmploymentGenderEnum(enum.Enum):
    default = 'default'
    male = 'male'
    female = 'female'
class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	full_name = db.Column(db.String(64), index=True, unique=True)
	email = db.Column(db.String(120), index=True, unique=True)
	password_hash = db.Column(db.String(128))
	address = db.Column(db.String(120), nullable=False)
	gender = db.Column(
		db.Enum(EmploymentGenderEnum), 
        	default="-",
        	nullable=False
	)

	def __repr__(self):
	    return '<User {}>'.format(self.full_name)
class Instituicao(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64), index=True, unique=True)
	email = db.Column(db.String(120), index=True, unique=True)
	address = db.Column(db.String(120), nullable=False)

	def __repr__(self):
	    return '<Name {}>'.format(self.name)
