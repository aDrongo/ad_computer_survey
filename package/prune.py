import logging
import json
import sys
import os
import modules.database as database
import modules.ldap as ldap
import modules.pingdevice as pingdevice
from modules.assorted import getLocation, getGroup, compare, loadConfig


def difference(data,ldap_results):
    table_devices = []
    ldap_devices = []
    for device in data:
        table_devices.append(device.id)
    for device in ldap_results:
        if compare(search_filter_Env, device.distinguishedName):
            ldap_devices.append(device.cn.value)
    diff = set(table_devices) - set(ldap_devices)
    return diff


def prune(data):
    i = 0
    for device in data:
        i = i + 1
        logging.debug(f'deleting {device}')
        session.query(Table).filter_by(id=f'{device}').delete()
    try:
        session.commit()
        logging.debug(f'Deleted {i} devices from DB')
        result = f'Deleted {i} devices from DB'
    except:
        session.rollback()
        logging.debug(f'Failed to delete devices from DB')
        result = f'Failed to delete devices from DB'
    session.close()
    return result


logging.basicConfig(filename=f'errors.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logging.debug('Running Prune')

# Load Config
try:
    (server_Env,
    database_Env,
    user_name_Env,
    user_pass_Env,
    workers_Env,
    search_base_Env,
    search_attributes_Env,
    search_filter_Env,
    subnet_dict_Env) = loadConfig()
except Exception as e:
    logging.error(e)
    sys.exit(1)


engine, connection, session, metadata = database.connect_db(database_Env)
data = session.query(database.Table).all()
ldap_results = ldap.search(server_Env, user_name_Env, user_pass_Env, search_base_Env, search_attributes_Env, "(objectClass=computer)")
diff = difference(data,ldap_results)
result = prune(diff)
print(result)

logging.debug('Completed Prune')
