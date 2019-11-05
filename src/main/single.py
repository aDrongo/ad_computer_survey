import time
import subprocess
import re
import logging
import json
import sys
import sqlalchemy as db
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from ldap_search.ldap_search import ldap_search

current_Time = time.strftime("%Y%m%d-%H%M%S")
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
    lastlogon = db.Column(db.String())
    os = db.Column(db.String())
    version = db.Column(db.String())


# Define Database to connect to. Will create if empty
def connect_db():
    engine = db.create_engine(f'sqlite:///{database_EnvVariable}')
    connection = engine.connect()
    Session = sessionmaker(bind=engine)
    session = Session()
    metadata = db.MetaData()
    Base.metadata.create_all(engine)
    return engine, connection, session, metadata


# Filter
def compare(filter, data):
    if str(filter) in str(data):
        logging.debug('true')
        return True
    else:
        logging.debug('false')
        return False


def ping_translate(returncode, ping_result):
    # This is the asynchronous command that it will wait for
    if returncode == 0:
        try:
            ping_result_ip = (re.search(r'\d+\.\d+\.\d+\.\d+', str(ping_result))).group(0)
        except:
            ping_result_ip = 0
        try:
            subnet_ip = (re.search(r'\d+\.\d+\.\d+', str(ping_result))).group(0)
        except:
            subnet_ip = '0.0.0.0'
        try:
            ping_result_time = str((re.search(r'time=\d+\.\d+', str(ping_result))).group(0)).replace("time=","")
        except:
            ping_result_time = str("0.0")
    else:
        subnet_ip = '0.0.0.0'
        ping_result_ip = 0
        ping_result_time = 0.0
    return ping_result_ip, ping_result_time, subnet_ip


def update_db(device,session):
    ping = subprocess.run(['ping', f'{device.dnsHostName}', '-c 1', '-w 2', '-4'], capture_output=True)
    if int(ping.returncode) != 0:
        ping = subprocess.run(['ping', f'{device.dnsHostName}', '-c 1', '-w 2', '-6'], capture_output=True)
    ping_result = ping.stdout.decode()
    ping_result = str(ping_result) + str(ping.stderr.decode())
    ping_result_returncode = int(ping.returncode)
    ping_result_ip, ping_result_time, subnet_ip = ping_translate(ping_result_returncode, ping_result)
    #Now formats and adds to DB
    if (len(device.location.values) == 0) or (device.location == 'unknown'):
        location = subnet_dict_EnvVariable.get(f"{subnet_ip}", 'unknown')
    else:
        location = device.location
    group = str((re.search(r'OU=\w+\s*\w*', str(device.distinguishedName))).group(0)).replace("OU=","")
    data = [{'id': str(device.cn),
             'ip': str(ping_result_ip),
             'ping_code': int(ping_result_returncode),
             'ping_time': float(ping_result_time),
             'time_stamp': str(current_Time),
             'description': str(device.description),
             'location': str(location),
             'group': str(group),
             'tv': str(device.telephoneNumber),
             'lastlogon': str(device.lastLogonTimestamp)[:16],
             'os': str(device.operatingSystem),
             'version': str(device.operatingSystemVersion)}]
    existing_result = session.query(Table).filter_by(id=f'{device.cn}').count()
    if existing_result > 0:
        session.bulk_update_mappings(Table, data)
        try:
            session.commit()
        except:
            session.rollback()
            raise
    else:
        session.bulk_insert_mappings(Table, data)
        try:
            session.commit()
        except:
            session.rollback()
            raise
    pass


# This is the main function
def main(filter):
    search_filter = f"(cn={filter})"
    ldap_result = ldap_search(server_EnvVariable, user_name_EnvVariable, user_pass_EnvVariable, search_base_EnvVariable, search_attributes_EnvVariable ,search_filter)
    engine, connection, session, metadata = connect_db()
    print(session)
    for device in ldap_result:
        if compare(filter, device):
            update_db(device,session)
        pass


# Argument is device to filter for
main(sys.argv[1])
