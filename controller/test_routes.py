from flask import Request, request
import requests

# Importamos a biblioteca de testes
import unittest

class ApiTest(unittest.TestCase):
    API_URL = "http://127.0.0.1:5000/api"
    INSTITUTION_URL = "{}/instituicao".format(API_URL)
    INSTITUTION_OBJ = {
        "_id": "61ef06b988cc574cb38233d3",
        "name": "Instituticao Test",
        "email": "testinstitution@gmail.com",
        "address": "Rua Teste da Silva",
        "url": "https://www.testeinstituicao.com.br",
        "cep": "10027125",
        "phone_number": "013995620326"
    }

    # GET request to /api/instituicao returns the details of all institutions
    def test_1_get_all_institutitons(self):
        r = requests.get(ApiTest.INSTITUTION_URL)
        self.assertEqual(200, r.status_code)
        self.assertEqual(4, len(r.json()))

    # POST request to /api/instituicao to create a new institution object
    def test_2_post_institution(self):
        r = requests.post(ApiTest.INSTITUTION_URL, json=ApiTest.INSTITUTION_OBJ)
        self.assertEqual(201, r.status_code)

    def test_3_get_institution_by_id(self):
        id = "61ef06b988cc574cb38233d3"
        r = requests.get("{}/{}").format(ApiTest.API_URL, id)
        self.assertEqual(200, r.status_code)
        self.assertDictEqual(r.json(),ApiTest.INSTITUTION_OBJ)
        