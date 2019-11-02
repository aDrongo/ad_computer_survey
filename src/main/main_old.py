# import ping
from ldap_search.ldap_search import ldap_search
from ping.ping import ping
import sqlalchemy as db
import time
import asyncio

server_EnvVariable = "nwmsdc400.internal.northwestmotorsportinc.com"
user_name_EnvVariable = "nwms\\ben.gardner"
user_pass_EnvVariable = "jumPingmotorsport1"
search_base_EnvVariable = 'OU=NWMS Computers,DC=internal,DC=northwestmotorsportinc,DC=com'

engine = db.create_engine('sqlite:///database.sqlite')
connection = engine.connect()
metadata = db.MetaData()

table = db.Table('table', metadata,
                db.Column('id', db.String()),
                db.Column('ip', db.String()),
                db.Column('ping_code', db.Integer()),
                db.Column('ping_time', db.Float()),
                db.Column('time_stamp', db.String()))
metadata.create_all(engine)
insert_query = db.insert(table)
update_query = db.update(table)

current_Time = time.strftime("%Y%m%d-%H%M%S")

ldap_result = ldap_search(server_EnvVariable, user_name_EnvVariable, user_pass_EnvVariable, search_base_EnvVariable)
for device in ldap_result:
    ping_result = ping(dnsName=str(device.dnsHostName))
    data = [{'id': str(device.cn),
                     'ip': str(ping_result.ip),
                     'ping_code': int(ping_result.returncode),
                     'ping_time': float(ping_result.time),
                     'time_stamp': str(current_Time)}]
    select_query = f"SELECT id FROM 'table' WHERE id = {str(device.cn)}"
    try:
        select_result = connection.execute(select_query).scalar()
    except:
        select_result = False
    if select_result is not False:
        insert_result = connection.exectue(update_query, data)
    else:
        insert_result = connection.execute(insert_query, data)

results = connection.execute(db.select([table])).fetchall()
print(results)
new_Time = time.strftime("%Y%m%d-%H%M%S")
print(current_Time)
print(new_Time)
