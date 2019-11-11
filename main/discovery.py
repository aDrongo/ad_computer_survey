import time
import asyncio
import re
import logging
import json
import sys
import os
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
def compare(filters, data):
    for filter in filters:
        if str(filter) not in str(data):
            pass
        else:
            return False
    return True


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


# Primary function, pings device then adds to dbnot
async def update_db(device):
    # This is the asynchronous command that it will wait for
    ping_async = await asyncio.create_subprocess_exec('ping', f'{device.dnsHostName}', '-c 1', '-w 2', '-4', stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    stdout, stderr = await ping_async.communicate()
    if stdout:
        ping_result = stdout.decode()
    if stderr:
        ping_result = stderr.decode()
    ping_result_returncode = int(ping_async.returncode)
    # If not found, try again on IPv6
    if ping_result_returncode == 2:
        ping_async = await asyncio.create_subprocess_exec('ping', f'{device.dnsHostName}', '-c 1', '-w 2', '-6', stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
        stdout, stderr = await ping_async.communicate()
        if stdout:
            ping_result = stdout.decode()
        if stderr:
            ping_result = stderr.decode()
        ping_result_returncode = int(ping_async.returncode)
    ping_result_ip, ping_result_time, subnet_ip = ping_translate(ping_result_returncode, ping_result)
    # Now formats and adds to DB
    if (len(device.extensionAttribute2.values) == 0) or (device.extensionAttribute2 == 'unknown'):
        location = subnet_dict_EnvVariable.get(f"{subnet_ip}", 'unknown')
    else:
        location = device.extensionAttribute2
    group = str((re.search(r'OU=\w+\s*\w*', str(device.distinguishedName))).group(0)).replace("OU=","")
    data = [{'id': str(device.cn),
             'ip': str(ping_result_ip),
             'ping_code': int(ping_result_returncode),
             'ping_time': float(ping_result_time),
             'time_stamp': str(current_Time),
             'description': str(device.description),
             'location': str(location),
             'group': str(group),
             'tv': str(device.extensionAttribute3),
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

# This is the worker function that works the queue and calls the primary function
async def worker(name, queue):
    while True:
        device = await queue.get()
        if compare(search_filter_EnvVariable, device.distinguishedName):
            print(f'Checking {device.distinguishedName}')
            await update_db(device)
            print(f'done with {device.distinguishedName}')
        queue.task_done()

# This is the main function that creates a Q and creates workers to work it
async def main(ldap_result):
    queue = asyncio.Queue()
    for device in ldap_result:
        queue.put_nowait(device)
    logging.debug("Q size:" + str(queue.qsize()))
    print("Q size:" + str(queue.qsize()))
    tasks = []
    for i in range(8):
        task = asyncio.create_task(worker(f"worker-{i}", queue))
        tasks.append(task)

    await queue.join()

    for task in tasks:
        task.cancel()

    await asyncio.gather(*tasks, return_exceptions=True)
    print('done')

# Get computers
ldap_result = ldap_search(server_EnvVariable, user_name_EnvVariable, user_pass_EnvVariable, search_base_EnvVariable, search_attributes_EnvVariable, "(objectClass=computer)")

# Connect to DB
engine, connection, session, metadata = connect_db()

# Add computers to DB
asyncio.run(main(ldap_result))

end_Time = time.strftime("%Y%m%d-%H%M%S")
logging.debug('start time' + str(current_Time))
logging.debug('finish time' + str(end_Time))
