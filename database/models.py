from datetime import datetime
import enum
import mongoengine as me


class GenderEnum(enum.Enum):
    MALE = 'male'
    FEMALE = 'female'


class User(me.Document):
    
     created_at = me.DateTimeField(default=datetime.utcnow)
     updated_at = me.DateTimeField(default=datetime.utcnow)
     username = me.StringField(required=True)
     email = me.EmailField(unique=True, required=True)
     password = me.StringField()
     address = me.StringField(required=True)
     phone_number = me.StringField(required=True)
     gender = me.EnumField(GenderEnum, required=True)
     def to_json(self):
        return {
            "_id": str(self.pk),
            "name": self.full_name,
            "email": self.email,
		    "address": self.address,
		    "phone_number": self.phone_number,
		    "gender": self.gender}


class Instituicao(me.Document):

    name = me.StringField()
    email = me.EmailField(unique=True, required=True)
    address = me.StringField(required=True)
    url = me.URLField()
    cep = me.StringField()
#   testar o armazenamento de imagens posteriormente.
#   image = me.ImageField(size=(800, 600, True))
    phone_number = me.StringField(required=True)

    def to_json(self):
        return {
                "_id": str(self.pk),
                "name": self.name,
                "email": self.email,
		        "address": self.address,
                "url": self.url,
                "cep": self.cep,
		        "phone_number": self.phone_number,
		        }