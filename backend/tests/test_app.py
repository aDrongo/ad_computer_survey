import os
import json
import pytest
from app import AppInitializer

def login(username):
    from modules.tools import get_token
    return get_token(username)

token = login('admin')

@pytest.fixture
def client():
    lds = AppInitializer()
    lds.set_configuration()
    lds.db_path('testing.sqlite')

    with lds.app.test_client() as client:
        with lds.app.app_context():
            lds.db_init()
            lds.db_create()
            lds.register_views()
            lds.configure_admin('testing1234')
        yield client

    try:
        os.remove('testing.sqlite')
    except FileNotFoundError:
        pass

def test_devices(client):
    assert len(json.loads(client.get('/api/devices').data)) == 0

def test_device(client):
    resp = client.post('/api/device/localhost', headers={'Authorization':token})
    #Post
    assert resp.status_code == 200
    assert json.loads(resp.data)['ip'] == "127.0.0.1"
    #Get
    assert client.get('/api/device/localhost', headers={'Authorization':token}).status_code == 200
    assert len(json.loads(client.get('/api/devices').data)) == 1
    #Delete
    assert client.delete('/api/device/localhost', headers={'Authorization':token}).status_code == 200
    assert len(json.loads(client.get('/api/devices').data)) == 0

def test_locations(client):
    resp = client.get('/api/locations', headers={'Authorization':token})
    data = json.loads(resp.data)
    assert resp.status_code == 200
    assert type(data) == type([])
    assert "Global" in data

#def test_scans(client):
#    client.post('/api/device/localhost', headers={'Authorization':token})
#    resp = client.get('/api/scan')
#    assert resp.status_code == 200
#    assert type(json.loads(resp.data)) == type([])

def test_scan(client):
    client.post('/api/device/localhost', headers={'Authorization':token})
    resp = client.get('/api/scan/localhost')
    assert resp.status_code == 200
    assert json.loads(resp.data)['ip'] == "127.0.0.1"

def test_history(client):
    resp = client.get('/api/history')
    assert resp.status_code == 200
    assert type(json.loads(resp.data)) ==  type([])

def test_history(client):
    client.post('/api/device/localhost', headers={'Authorization':token})
    resp = client.get('/api/history/localhost')
    data = json.loads(resp.data)
    assert resp.status_code == 200
    assert type(data) ==  type([])
    assert data[0]['device'] == 'localhost'

def test_login(client):
    #Get
    resp = client.get('/api/login', headers={'Authorization':token})
    assert resp.status_code == 200
    resp = client.get('/api/login', headers={'Authorization':'1'})
    assert resp.status_code == 210
    #Post
    resp = client.post('/api/login', headers={'username':'admin','password':'testing1234'})
    assert resp.status_code == 200
    assert json.loads(resp.data)['token'] != None

def test_users(client):
    #Get
    resp = client.get('/api/users', headers={'Authorization':token})
    assert resp.status_code == 200
    assert type(json.loads(resp.data)) == type([])
    #Post
    resp = client.post('/api/users', headers={'username':'tester','password':'testing','Authorization':token})
    assert resp.status_code == 200
    assert json.loads(resp.data) != False
    #Delete
    resp = client.delete('/api/users', headers={'username':'tester','Authorization':token})
    assert resp.status_code == 200
    assert json.loads(resp.data).get('message') != None