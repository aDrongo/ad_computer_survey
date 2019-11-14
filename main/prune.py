import logging
import json
import sys
import os
import sqlalchemy as db
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from ldap_search.ldap_search import ldap_search

logging.basicConfig(filename=f'errors.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Load Config
try:
    with open('config.json') as f:
        config = json.loads(f.read())
    try:
        server_EnvVariable = str(config['server_EnvVariable'])
        database_EnvVariable = str(config['database_EnvVariable'])
        user_name_EnvVariable = str(config['user_name_EnvVariable'])
        user_pass_EnvVariable = str(config['user_pass_EnvVariable'])
        search_base_EnvVariable = str(config['search_base_EnvVariable'])
        search_attributes_EnvVariable = config['search_attributes_EnvVariable']
        search_filter_EnvVariable = config['search_filter_EnvVariable']
        subnet_dict_EnvVariable = config['subnet_dict_EnvVariable']
    except Exception as e:
        logging.debug(e)
        sys.exit('Config file incorrect')
except Exception as e:
    logging.debug(e)
    print(os.getcwd())
    sys.exit('Config file not loaded')


# For class to create table
Base = declarative_base()


# Defines table for SqlAlchemy
class Table(Base):
    __tablename__ = 'table'
    id = db.Column(db.String(), primary_key=True)
    ip = db.Column(db.String())
    ping_code = db.Column(db.Integer())
    ping_time = db.Column(db.Float())
    time_stamp = db.Column(db.String())
    description = db.Column(db.String())
    location = db.Column(db.String())
    group = db.Column(db.String())
    tv = db.Column(db.String())
    lastup = db.Column(db.String())
    lastlogon = db.Column(db.String())
    os = db.Column(db.String())
    version = db.Column(db.String())


# Filter
def compare(filters, data):
    for filter in filters:
        if str(filter) not in str(data):
            pass
        else:
            return False
    return True


def connect_db():
    try:
        engine = db.create_engine(f'sqlite:///{database_EnvVariable}', connect_args={'check_same_thread': False})
        connection = engine.connect()
        Session = sessionmaker(bind=engine)
        session = Session()
        print('Connected to DB')
    except Exception as e:
        print(e)
        sys.exit(e)
    return session


def difference(data):
    table_devices = []
    ldap_devices = []
    for device in data:
        table_devices.append(device.id)
    for devices in ldap_result:
        if compare(search_filter_EnvVariable, devices.distinguishedName):
            ldap_devices.append(devices.cn.value)
    diff_devices = set(table_devices) - set(ldap_devices)
    return diff_devices

def prune(data):
    for device in data:
        print(f'deleting {device}')
        session.query(Table).filter_by(id=f'{device}').delete()
    session.commit()
    session.close()



session = connect_db()
data = session.query(Table).all()
ldap_result = ldap_search(server_EnvVariable, user_name_EnvVariable, user_pass_EnvVariable, search_base_EnvVariable, search_attributes_EnvVariable, "(objectClass=computer)")
diff = difference(data)
prune(diff)
