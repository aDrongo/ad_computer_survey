from ldap_search.ldap_search import ldap_search
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import sqlalchemy as db
import time
import asyncio
import subprocess
import re
import logging
import json
import sys


current_Time = time.strftime("%Y%m%d-%H%M%S")
logging.basicConfig(filename=f'ping_survey_{current_Time}.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

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
        search_filter_EnvVariable = config['search_filter_EnvVariable']
        subnet_dict_EnvVariable = config['subnet_dict_EnvVariable']
    except Exception as e:
        logging.debug(e)
        sys.exit('Config file incorrect')
except Exception as e:
    logging.debug(e)
    sys.exit('Config file not loaded')


Base = declarative_base()


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

#    table = db.Table('table', metadata,
#                    db.Column('id', db.String(), primary_key=True),
#                    db.Column('ip', db.String()),
#                    db.Column('ping_code', db.Integer()),
#                    db.Column('ping_time', db.Float()),
#                    db.Column('time_stamp', db.String()),
#                    db.Column('description', db.String()),
#                    db.Column('location', db.String()),
#                    db.Column('group', db.String()),
#                    db.Column('lastlogon', db.String()),
#                    db.Column('OS', db.String()),
#                    db.Column('Version', db.String()))
    Base.metadata.create_all(engine)
#    insert_query = db.insert(table)
#    update_query = db.update(table)
    return engine, connection, session, metadata # , table, insert_query, update_query


def compare(filters, data):
    for filter in filters:
        if str(filter) not in str(data):
            pass
        else:
            return False
    return True


# Primary function, pings device then adds to dbnot
async def update_db(device):
    dnsName = str(device.dNSHostName)
    logging.debug(f'Starting {dnsName}')
    # This is the asynchronous command that it will wait for
    ping_async = await asyncio.create_subprocess_exec('ping', f'{dnsName}', '-c 1', '-w 2', '-4', stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    logging.debug('waiting on ping_async')
    stdout, stderr = await ping_async.communicate()
    logging.debug('finished waiting')
    if stdout:
        ping_result = stdout.decode()
    if stderr:
        ping_result = stderr.decode()
    ping_result_returncode = int(ping_async.returncode)
    logging.debug(f"returncode:{ping_result_returncode}")
    # Get details from ping result
    if ping_result_returncode == 0:
        ping_result_ip = (re.search(r'\d+\.\d+\.\d+\.\d+', str(ping_result))).group(0)
        subnet_ip = (re.search(r'\d+\.\d+\.\d+', str(ping_result))).group(0)
        logging.debug(f'Trying to find subnet {subnet_ip}')
        location = subnet_dict_EnvVariable.get(f"{subnet_ip}", 'unknown')
        logging.debug(location)
        try:
            ping_result_time = str((re.search(r'time=\d+\.\d+', str(ping_result))).group(0)).replace("time=","")
        except:
            ping_result_time = str("0.0")
    else:
        location = 'unknown'
        ping_result_ip = 0
        ping_result_time = 0.0
    logging.debug("ping proccessed")
    # Now formats and adds to DB
    group = str((re.search(r'OU=\w+\s\w+', str(device.distinguishedName))).group(0)).replace("OU=","")
    data = [{'id': str(device.cn),
             'ip': str(ping_result_ip),
             'ping_code': int(ping_result_returncode),
             'ping_time': float(ping_result_time),
             'time_stamp': str(current_Time),
             'description': str(device.description),
             'location': str(location),
             'group': str(group),
             'lastlogon': str(device.lastLogonTimestamp),
             'os': str(device.operatingSystem),
             'version': str(device.operatingSystemVersion)}]
    logging.debug('trying to find existing id')
    existing_result = session.query(Table).filter_by(id=f'{device.cn}').count()
    if existing_result > 0:
        logging.debug('updating row')
        session.bulk_update_mappings(Table, data)
        try:
            session.commit()
        except:
            session.rollback()
            raise
    else:
        logging.debug('inserting row')
        session.bulk_insert_mappings(Table, data)
        try:
            session.commit()
        except:
            session.rollback()
            raise
        # insert_result = connection.execute(insert_query, data)
    logging.debug(f'finished {dnsName}')
    pass

# This is the worker function that works the queue and calls the primary function
async def worker(name, queue):
    while True:
        device = await queue.get()
        logging.debug(f'Q for device {device.dNSHostName}')
        if compare(search_filter_EnvVariable, device.distinguishedName):
            logging.debug(f'processing {device.dNSHostName}')
            await update_db(device)
        logging.debug(f"Q done for {device.dNSHostName}")
        queue.task_done()

# This is the main function that creates a Q and creates workers to work it
async def main(ldap_result):
    queue = asyncio.Queue()
    for device in ldap_result:
        queue.put_nowait(device)
    logging.debug("Q size:" + str(queue.qsize()))
    tasks = []
    for i in range(8):
        task = asyncio.create_task(worker(f"worker-{i}", queue))
        tasks.append(task)

    await queue.join()

    for task in tasks:
        task.cancel()

    await asyncio.gather(*tasks, return_exceptions=True)

# Get LDAP computers
ldap_result = ldap_search(server_EnvVariable, user_name_EnvVariable, user_pass_EnvVariable, search_base_EnvVariable)

# Connect to DB
engine, connection, session, metadata = connect_db() # , table, insert_query, update_query


# Add computers to DB
asyncio.run(main(ldap_result))

end_Time = time.strftime("%Y%m%d-%H%M%S")
logging.debug('start time' + str(current_Time))
logging.debug('finish time' + str(end_Time))
