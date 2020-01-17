import time
import subprocess
import re
import logging
import json
import sys
import os
import asyncio
import modules.database as database
import modules.ldap as ldap
from modules.assorted import getLocation, getGroup, compare, loadConfig

#Create backlog queue and fill with fitlered ldap results
async def queue(ldap_results):
    queue = asyncio.Queue()
    for device in ldap_results:
        if compare(search_filter_Env, device.distinguishedName):
            queue.put_nowait(device)
    logging.debug("Q size:" + str(queue.qsize()))
    print("Q size:" + str(queue.qsize()))
    
    #Create work queue
    tasks = []
    #Create workers to work work queue
    for i in range(int(workers_Env)):
        task = asyncio.create_task(worker(f"worker-{i}", queue))
        tasks.append(task)

    #Block until queue is completed
    await queue.join()

    #Finish
    end_DateTime = time.monotonic()
    dif_Time = int(end_DateTime - current_DateTime)
    print(f'completed in {dif_Time} seconds')
    logging.debug(f'Completed in {dif_Time} seconds')

    pass


# This is the worker function that works the queue and calls the primary function
async def worker(name, queue):
    while True:
        device = await queue.get()
        await surveydevice(device)
        print(f'done with {device.distinguishedName}')
        queue.task_done()

# This is main function workers will call
async def surveydevice(device):
    #async wait on ping results
    ping_result_ip, ping_result_time, subnet_ip, ping_result_returncode = await apingdevice(device.dnsHostname)
    #Get location and group
    location = getLocation(device,subnet_ip,subnet_dict_Env)
    group = getGroup(device)
    #Update database
    result = database.update_db(
        device.cn,
        ping_result_ip,
        ping_result_returncode,
        ping_result_time,
        current_Time,
        device.description,
        location,
        group,
        device.extensionAttribute3,
        str(device.lastLogonTimestamp)[:16],
        device.operatingSystem,
        device.operatingSystemVersion,
        session)
    #If failed, let user know
    if not result:
        logging.debug(f"{device.cn} failed to update")
        print((f"{device.cn} failed to update"))

#Async Ping and translate
async def apingdevice(device):
    ping_async = await asyncio.create_subprocess_exec(
        'ping',
        f'{device}',
        '-c 1',
        '-w 2',
        '-4',
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE)
    stdout, stderr = await ping_async.communicate()
    if stdout:
        ping_result = stdout.decode()
    elif stderr:
        ping_result = stderr.decode()
    ping_result_returncode = int(ping_async.returncode)
    #Translate
    if ping_result_returncode == 0:
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
    return ping_result_ip, ping_result_time, subnet_ip, ping_result_returncode


if __name__ == "__main__":
    #Initialize
    current_Time = time.strftime("%Y-%m-%d %H:%M")
    current_DateTime = time.monotonic()
    logging.basicConfig(filename=f'errors.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
    logging.debug('Running Discovery')

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

    #Connect to database
    engine, connection, session, metadata = database.connect_db(database_Env)
    logging.debug('Connected to DB')

    #Get LDAP results
    ldap_results = ldap.search(server_Env, user_name_Env, user_pass_Env, search_base_Env, search_attributes_Env, "(objectClass=computer)")
    logging.debug('LDAP completed')

    #Run Async
    asyncio.run(queue(ldap_results))