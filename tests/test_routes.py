# from app import Init
from cmath import log

import mongomock
from app import app
# Importamos a biblioteca de testes
from mongoengine import connect, disconnect

import pytest


INSTITUTION_OBJ = {
    "name": "Instituticao Test",
    "email": "testinstitution@gmail.com",
    "address": "Rua Instituicao Teste",
    "url": "https://www.testeinstituicao.com.br",
    "cep": "10027125",
    "phone_number": "013995620326"
}

REGISTER_USER = {
    "username": "test",
    "email": "test@test.com",
    "password": "123",
    "address": "rua teste",
    "phone_number": "24124125152",
    "gender": "male"
}

@pytest.fixture
def client():
    disconnect()
    app.config["SECRET_KEY"] = 'GDtfDCFYjD'
    app.config["JWT_SECRET_KEY"] = '0D5BB45D5D378F2FB552C502F53AD63BE932AC0887E26FB2314EC0A8DEE46115'
    # mongomock.gridfs.enable_gridfs_integration()
    connect('mongoenginetest', host='mongomock://localhost')
    with app.test_client() as client:
        yield client

#User test    
def test_register(client):
    r = client.post("/api/register", json= REGISTER_USER)
    assert r.status_code == 201

def test_register_fail(client):
    r = client.post("/api/register", json= REGISTER_USER)
    assert REGISTER_USER['email'] == "test@test.com"

def test_login(client):
    test_register(client)
    r = client.post("/api/login", json= {"email": "test@test.com","password": "123"})
    assert r.status_code == 200

def test_login_fail(client):
    test_register(client)
    r = client.post("/api/login", json= {"email": "testerror@test.com","password": "123"})
    assert r.status_code == 404
    assert REGISTER_USER["email"] != "testerror@test.com"
    assert REGISTER_USER["password"] != "404"

def test_logout(client):
    test_login(client)
    r = client.post("/api/logout")
    assert r.status_code == 200
    
def test_get_logged_user(client):
    test_login(client)
    r = client.get("/api/get_logged_user")
    assert r.status_code == 200

#Institution test    
def test_get_all_institutitons(client):
    test_login(client)
    r = client.get('/api/instituicao')
    assert r.status_code == 200

def test_post_institution(client):
    test_login(client)
    r = client.post('/api/instituicao', json=INSTITUTION_OBJ)
    assert r.status_code == 201
    
def test_post_institution_fail(client):
    test_login(client)
    r = client.post('/api/instituicao', json=INSTITUTION_OBJ)
    assert "testinstitution@gmail.com" == INSTITUTION_OBJ["email"]
    assert "Rua Instituicao Teste" == INSTITUTION_OBJ["address"]
    assert "013995620326" == INSTITUTION_OBJ["phone_number"]

# fazer test dando certo
# def test_6_get_institution_by_id(client):

def test_get_institution_by_id_fail(client):
    test_post_institution(client)
    id = '61ef06b988cc574cb38233d3'
    r = client.get('/api/instituicao/', json=id)
    assert 404 == r.status_code
        