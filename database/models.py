from datetime import datetime
import enum
from typing_extensions import Required
import mongoengine as me

from controller.institution import Institution


class GenderEnum(enum.Enum):
    MALE = 'male'
    FEMALE = 'female'


class User(me.Document):
    
     created_at = me.DateTimeField(default=datetime.utcnow)
     updated_at = me.DateTimeField(default=datetime.utcnow)
     username = me.StringField(required=True)
     is_admin = me.BooleanField(default=False)
     icon = me.FileField()
     email = me.EmailField(unique=True, required=True)
     password = me.StringField()
     address = me.StringField(required=True)
     phone_number = me.StringField(required=True)
     gender = me.EnumField(GenderEnum, required=True)
     def to_json(self):
        return {
            "_id": str(self.pk),
            "name": self.username,
            "isAdmin": self.is_admin,
            "email": self.email,
		    "address": self.address,
		    "phone_number": self.phone_number,
		    "gender": self.gender}

#- TODO ->  lagitude e longitude - double (edited)

class InstitutionEnum(enum.Enum):

    ONG = 'ong'
    IGREJA_CATOLICA = 'igreja_catolica'
    IGREJA_PROTESTANTE = 'igreja_protestante'
    CARIDADE = 'caridade'

class Instituicao(me.Document):

    name = me.StringField()
    email = me.EmailField(unique=True, required=True)
    address = me.StringField(required=True)
    institution_type = me.EnumField(InstitutionEnum, required=True)  
    url = me.URLField()
    cep = me.StringField()
    image = me.URLField()
    phone_number = me.StringField(required=True)

    def to_json(self):
        return {
                "_id": str(self.pk),
                "name": self.name,
                "email": self.email,
		        "address": self.address,
                "url": self.url,
                "cep": self.cep,
                "image": self.image,
                "institution_type": self.institution_type,
		        "phone_number": self.phone_number,
		        }