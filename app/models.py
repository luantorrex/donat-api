# import datetime
# from enum import unique

# from flask.sessions import NullSession
# from marshmallow.fields import Boolean
# from app import db, ma
# import enum
# import json
# from dataclasses import dataclass
# from flask import jsonify
# from sqlalchemy_utils import PhoneNumber, PasswordType, URLType

# class EmploymentGenderEnum(enum.Enum):
#     male = 'male'
#     female = 'female'

# @dataclass
# class User(db.Model):
# 	id: int
# 	full_name: str
# 	email: str
# 	password_hash: str
# 	address : str 
# 	gender: str
# 	phone_number: int

# 	__tablename__ = 'user'
# 	id = db.Column(db.Integer, primary_key=True)
# 	admin = db.Column(db.Boolean, nullable=False)
# 	created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
#    	updated = db.Column(db.DateTime, onupdate=datetime.utcnow)
# 	full_name = db.Column(db.String(64), index=True, unique=True)
# 	email = db.Column(db.String(120), index=True, unique=True)
# 	password_hash = db.Column(PasswordType(
# 		schemes=[
# 		'pbkdf2_sha512',
# 		'md5_crypt'
# 		],
# 		deprecated=['md5_crypt']
# 	))
# 	address = db.Column(db.String(120), nullable=False)
# 	gender = db.Column(db.Enum(EmploymentGenderEnum), nullable=False)
# 	_phone_number = db.Column(db.Unicode(20))

# 	phone_number = db.composite(
# 		PhoneNumber,
# 		_phone_number,
#     	)

# 	def __repr__(self):
# 	    return '<User {}>'.format(self.full_name)

# class UserSchema(ma.Schema):
#     class Meta:
#         fields = ("id", "full_name", "email", "address", "gender", "phone_number")
 
# @dataclass
# class Instituicao(db.Model):
# 	id: int
# 	name: str
# 	email: str
# 	address : str 
# 	cep: str
	
# 	__tablename__ = 'instituicao'
# 	id = db.Column(db.Integer, primary_key=True)
# 	name = db.Column(db.String(64), index=True, unique=True)
# 	email = db.Column(db.String(120), index=True, unique=True)
# 	address = db.Column(db.String(120), nullable=False)
# 	url = db.Column(URLType)
# 	cep = db.Column(db.String(8), nullable=False)
# 	# criar coluna futura para armazenar imagem da instituicao
# 	_phone_number = db.Column(db.Unicode(20))

# 	phone_number = db.composite(
# 		PhoneNumber,
# 		_phone_number,
#     	)

# 	def __repr__(self):
# 	    return '<Name {}>'.format(self.name)