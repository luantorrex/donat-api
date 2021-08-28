from enum import unique
from app import db
import enum
import json
from dataclasses import dataclass
from flask import jsonify


class EmploymentGenderEnum(enum.Enum):
    male = 'male'
    female = 'female'

@dataclass
class User(db.Model):
	id: int
	full_name: str
	email: str
	password_hash: str
	address : str 
	gender: str

	id = db.Column(db.Integer, primary_key=True)
	full_name = db.Column(db.String(64), index=True, unique=True)
	email = db.Column(db.String(120), index=True, unique=True)
	password_hash = db.Column(db.String(128))
	address = db.Column(db.String(120), nullable=False)
	gender = db.Column(db.Enum(EmploymentGenderEnum), nullable=False)

	def __repr__(self):
	    return '<User {}>'.format(self.full_name)

@dataclass
class Instituicao(db.Model):
	id: int
	name: str
	email: str
	address : str 

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64), index=True, unique=True)
	email = db.Column(db.String(120), index=True, unique=True)
	address = db.Column(db.String(120), nullable=False)

	def __repr__(self):
	    return '<Name {}>'.format(self.name)
