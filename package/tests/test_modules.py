import sys 
sys.path.append('..')
import os
import pytest
import modules.database as database
import modules.ldap as ldap
import modules.pingdevice as pingdevice
from modules.assorted import getLocation, getGroup, compare, loadConfig
import sqlalchemy as db
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from modules.database import Base, Table

class extensionAttribute2:
    def __init__(self):
        self.values = (0,)
        self.value = 'unknown'

class Device:
    def __init__(self):
        self.value = 0
        self.name = 'localhost'
        self.extensionAttribute2 = extensionAttribute2()
        self.distinguishedName = 'CN=CTVM01,OU=Early Updates,OU=Computers,DC=internal,DC=contoso,DC=com'

device = Device()

try:
    (server_Env,
    database_Env,
    user_name_Env,
    user_pass_Env,
    search_base_Env,
    search_attributes_Env,
    search_filter_Env,
    subnet_dict_Env) = loadConfig()
except Exception as e:
    print(f'loadConfig error:\n{e}')


def test_loadConfig():
        assert ('server_Env' in globals())
        assert ('user_name_Env' in globals())
        assert ('user_pass_Env'  in globals())
        assert ('search_base_Env'  in globals())
        assert ('search_attributes_Env' in globals())
        assert ('search_filter_Env' in globals())
        assert ('subnet_dict_Env' in globals())

def test_compare_false():
    assert compare([1,2,3],[3,4,5]) == False

def test_compare_true():
    assert compare([1,2,3],[4,5,6]) == True

def test_getLocation():
    assert getLocation(device,'10.0.0',subnet_dict_Env) == "Contoso"

def test_getGroup():
    assert getGroup(device) == 'Early Updates'

def test_pingdevice():
    ping_result_ip, ping_result_time, subnet_ip, ping_returncode = pingdevice.ping(device.name)
    assert ping_result_ip == '127.0.0.1'
    assert subnet_ip == '127.0.0'
    assert ping_returncode == 0
    
def test_Database():
    engine, connection, session, metadata = database.connect_db(database_Env)
    data = [{'id': str('test123'),
             'ip': str('127.0.0.1'),
             'ping_code': int(0),
             'ping_time': float(0),
             'time_stamp': str('0000-1111'),
             'description': str('Description'),
             'location': str('Location'),
             'group': str('Group'),
             'tv': str('TV'),
             'lastlogon': str('0000-1111'),
             'os': str('OS'),
             'version': str('Ver')},]
    session.bulk_insert_mappings(Table, data)
    try:
        session.commit()
        assert True
    except:
        session.rollback()
        assert False
    os.remove(database_Env)
