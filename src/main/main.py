# import ping
from ldap_search.ldap_search import ldap_search
import sqlalchemy as db
import time
import asyncio
import subprocess
import re
import logging

server_EnvVariable = "nwmsdc400.internal.northwestmotorsportinc.com"
database_EnvVariable = "database.sqlite"
user_name_EnvVariable = "nwms\\ben.gardner"
user_pass_EnvVariable = "jumPingmotorsport1"
search_base_EnvVariable = 'OU=NWMS Computers,DC=internal,DC=northwestmotorsportinc,DC=com'
search_filter_EnvVariable = 'OU=Retired Computers'
subnet_dict_EnvVariable = {
    "10.4.3": "Puyallup 400 ",
    "10.4.4": "Puyallup 1502",
    "10.4.5": "Puyallup 819",
    "10.4.6": "Lynnwood 17510",
    "10.4.7": "Puyallup 300",
    "10.4.8": "Puyallup 1830",
    "10.4.9": "Everet 12227",
    "10.4.16": "Pasco 816",
    "10.4.20": "Puyallup 500",
    "10.4.24": "Puyallup Joydrive",
    "10.4.28": "Lynnwood 17319",
    "10.4.3.32": "Marysville 3520",
    "10.4.36": "Spokane 12606",
    "172.16.0": "AWS",
    "0.0.0.0": "Unknown"
}
current_Time = time.strftime("%Y%m%d-%H%M%S")
logging.basicConfig(filename=f'{current_Time}.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

engine = db.create_engine(f'sqlite:///{database_EnvVariable}')
connection = engine.connect()
metadata = db.MetaData()

table = db.Table('table', metadata,
                db.Column('id', db.String()),
                db.Column('ip', db.String()),
                db.Column('ping_code', db.Integer()),
                db.Column('ping_time', db.Float()),
                db.Column('time_stamp', db.String()),
                db.Column('location', db.String()),
                db.Column('group', db.String()),
                db.Column('OS', db.String()),
                db.Column('Version', db.String()))
metadata.create_all(engine)
insert_query = db.insert(table)
update_query = db.update(table)


async def update_db(device):
    # Pings the device
    dnsName = str(device.dNSHostName)
    logging.debug(f'Starting {dnsName}')
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
    group = str((re.search(r'OU=\w+\s\w+', str(device.distinguishedName))).group(0)).replace("OU=","")
    data = [{'id': str(device.cn),
                     'ip': str(ping_result_ip),
                     'ping_code': int(ping_result_returncode),
                     'ping_time': float(ping_result_time),
                     'time_stamp': str(current_Time),
                     'group': str(group),
                     'location': str(location),
                     'OS': str(device.operatingSystem),
                     'Version': str(device.operatingSystemVersion)}]
    select_query = f"SELECT id FROM 'table' WHERE id = {str(device.cn)}"
    try:
        logging.debug('trying to find existing id')
        select_result = connection.execute(select_query).scalar()
    except:
        logging.debug('id not found')
        select_result = False
    if select_result is not False:
        logging.debug('updating row')
        insert_result = connection.exectue(update_query, data)
    else:
        logging.debug('inserting row')
        insert_result = connection.execute(insert_query, data)
    logging.debug(f'finished {dnsName}')
    pass


async def worker(name, queue):
    while True:
        device = await queue.get()
        logging.debug(f'Q for device {device.dNSHostName}')
        if not search_filter_EnvVariable in str(device.distinguishedName):
            logging.debug(f'processing {device.dNSHostName}')
            await update_db(device)
        logging.debug(f"Q done for {device.dNSHostName}")
        queue.task_done()


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

ldap_result = ldap_search(server_EnvVariable, user_name_EnvVariable, user_pass_EnvVariable, search_base_EnvVariable)

asyncio.run(main(ldap_result))

results = connection.execute(db.select([table])).fetchall()
new_Time = time.strftime("%Y%m%d-%H%M%S")
logging.debug('start time' + str(current_Time))
logging.debug('finish time' + str(new_Time))
