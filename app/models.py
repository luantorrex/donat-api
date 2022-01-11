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


class Instituicao(me.Document):

    name = me.StringField()
    email = me.EmailField(unique=True, required=True)
    address = me.StringField(required=True)
    url = me.URLField()
    cep = me.StringField()
#   testar o armazenamento de imagens posteriormente.
#   image = me.ImageField(size=(800, 600, True))
    phone_number = me.StringField(required=True)

#     def __repr__(self):
#         return '<Name {}>'.format(self.name)
    def to_json(self):
        return {"name": self.name,
                "email": self.email,
		        "address": self.address,
                "url": self.url,
                "cep": self.cep,
		        "phone_number": self.phone_number,
		        }