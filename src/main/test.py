from ldap_search.ldap_search import ldap_search
import sqlalchemy as db
from sqlalchemy.orm import sessionmaker
import time
import asyncio
import subprocess
import re
import logging
import json
import sys

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
        sys.exit('Config file incorrect')
except Exception as e:
    sys.exit('Config file not loaded')

def connect_db():
    engine = db.create_engine(f'sqlite:///{database_EnvVariable}')
    Session = sessionmaker(bind=engine)
    session = Session()
    connection = engine.connect()
    metadata = db.MetaData()
    table = db.Table('table', metadata,
                    db.Column('id', db.String(), primary_key=True),
                    db.Column('ip', db.String()),
                    db.Column('ping_code', db.Integer()),
                    db.Column('ping_time', db.Float()),
                    db.Column('time_stamp', db.String()),
                    db.Column('description', db.String()),
                    db.Column('location', db.String()),
                    db.Column('group', db.String()),
                    db.Column('lastlogon', db.String()),
                    db.Column('OS', db.String()),
                    db.Column('Version', db.String()))
    metadata.create_all(engine)
    insert_query = db.insert(table)
    update_query = db.update(table)
    return engine, connection, session, metadata, table, insert_query, update_query

engine, connection, session, metadata, table, insert_query, update_query = connect_db()

ldap_result = ldap_search(server_EnvVariable, user_name_EnvVariable, user_pass_EnvVariable, search_base_EnvVariable)

for device in ldap_result:
    print(device.cn)
    print(type(session.query(table).filter_by(id=f'{device.cn}').count()))
