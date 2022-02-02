import unittest
from mongoengine import connect, disconnect

from database.models import User


# class TestDB(unittest.TestCase):

#     # @classmethod
#     # def setUpClass(cls):
#     #     connect('mongoenginetest', host='mongomock://localhost')

#     # @classmethod
#     # def tearDownClass(cls):
#     #    disconnect()

#     def test_thing(self):
#         pers = User(username = 'John', email= 'test@gmail.com',
#                     password = 'test', address = 'rua teste 123', 
#                     phone_number = '13996131248', gender = 'male')
#         pers.save()

#         fresh_pers = User.objects().first()
#         assert fresh_pers.username ==  'John'
#         assert fresh_pers.email ==  'test@gmail.com'