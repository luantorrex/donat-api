# import datetime
# from marshmallow.fields import Boolean
from datetime import datetime
import enum
from bson.json_util import default
import mongoengine as me
# import json
# from dataclasses import dataclass
# from flask import jsonify


class GenderEnum(enum.Enum):
    MALE = 'male'
    FEMALE = 'female'


class User(me.Document):
#     __tablename__ = 'user'
     admin = me.BooleanField(default=0)
     created_at = me.DateTimeField(default=datetime.utcnow)
     updated_at = me.DateTimeField(default=datetime.utcnow)
     full_name = me.StringField(required=True)
     email = me.EmailField(unique=True, required=True)
     password = me.StringField()
     address = me.StringField(required=True)
     phone_number = me.StringField(required=True)
     gender = me.EnumField(GenderEnum, required=True)
     def to_json(self):
        return {"name": self.full_name,
                "email": self.email,
		"address": self.address,
		"phone_number": self.phone_number,
		"gender": self.gender}
#     def __repr__(self):
#         return '<User {}>'.format(self.full_name)


# class UserSchema(ma.Schema):
#     class Meta:
#         fields = ("id", "full_name", "email",
#                   "address", "gender", "phone_number")


# @dataclass
# class Instituicao(db.Model):
#     id: int
#     name: str
#     email: str
#     address: str
#     cep: str

#     __tablename__ = 'instituicao'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(64), index=True, unique=True)
#     email = db.Column(db.String(120), index=True, unique=True)
#     address = db.Column(db.String(120), nullable=False)
#     url = db.Column(URLType)
#     cep = db.Column(db.String(8), nullable=False)
#     # criar coluna futura para armazenar imagem da instituicao
#     db.ImageField(https://mongoengine-odm.readthedocs.io/apireference.html#mongoengine.fields.ImageField)
#     _phone_number = db.Column(db.Unicode(20))

#     phone_number = db.composite(
#         PhoneNumber,
#         _phone_number,
#     )

#     def __repr__(self):
#         return '<Name {}>'.format(self.name)
