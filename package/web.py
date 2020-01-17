from flask import Flask, render_template, Response, redirect, url_for
import sqlalchemy as db
from sqlalchemy.orm import sessionmaker
from collections import Counter
from jinja2 import Template
from apscheduler.schedulers.background import BackgroundScheduler
import os
import json
import operator
import sys
import time
import math
import logging
import logging.handlers
import modules.database as database
import modules.ldap as ldap
import modules.pingdevice as pingdevice
from modules.assorted import getLocation, getGroup, compare, loadConfig, convertRequest
from modules.database import Table, Base

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s', handlers=[logging.handlers.RotatingFileHandler("errors.log", maxBytes=1000000, backupCount=3)])

logging.info('Running web.py')

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

try:
    with open('config.json') as f:
        config = json.loads(f.read())
    try:
        user_name_Env2 = str(config['user_name_Env2'])
        user_pass_Env2 = str(config['user_pass_Env2'])
    except Exception as e:
        raise 'Config file incorrect'
except Exception as e:
    raise 'Config file not loaded'

header = """
<!DOCTYPE html>
<html>
 <head>
  <meta charset="utf-8" http-equiv="refresh" content="300" >
   <title>LDAP Device Surveyor</title>
    <style>
    ul { margin: 0; padding: 5px 5px 0 5px; float: left; }
    li { display: inline-block; padding: 2px 10px 2px 2px; color: #D9D8D6; vertical-align: middle; }
    html { 
        height: 100%;
        box-sizing: border-box;
    }
    body {
        background-color: #222222;
        color: white;
        font-family: monospace;
        min-height: 95%;
        position: relative;
        font-size: 10px;;
        margin: 0;
        padding: 50px 0 0 0;
      }
    a, a:link, a:visited, a:active {
        color: inherit;
        text-decoration: none;
      }
    a:hover{
        color: inherit;
        text-decoration: underline;
      }
    nav {
        position: fixed;
        margin: 0;
        font-size: 16px;
        background-color: #565557;
        width: 100%;
        overflow: hidden;
        box-sizing: border-box;
        display: inline-block;
        transition: all 0.2s;
        list-style-type: none;
        padding-left: 1%;
        top: 0;
    }
    </style>
 </head>
  <body>
    <nav>
      <ul>
        <li><img height="30px" src="https://cdn.nwmsrocks.com/img/3dc41c7.png"/></li>
        <li><a href="/">Overview</a></li>
      </ul>
    </nav>
    <div>
"""


def rename(var):
    if var == 0:
        return 'good'
    else:
        return 'bad'


app = Flask(__name__)


@app.route("/")
def home():
    try:
        engine = db.create_engine(f'sqlite:///{database_Env}', connect_args={'check_same_thread': False})
        connection = engine.connect()
        print('Connected to DB')
    except Exception as e:
        print(e)
        sys.exit(e)
    data = connection.execute("SELECT * FROM 'table' ORDER BY 'group' DESC;")
    data = data.fetchall()
    data.sort(key=operator.itemgetter(7))
    locations = connection.execute("SELECT DISTINCT location FROM 'table';")
    locations = locations.fetchall()
    locations.sort(key=operator.itemgetter(0))
    connection.close()
    return render_template("home.html", data=data, locations=locations)


@app.route("/iframe")
def iframe():
    try:
        engine = db.create_engine(f'sqlite:///{database_Env}', connect_args={'check_same_thread': False})
        connection = engine.connect()
        print('Connected to DB')
    except Exception as e:
        print(e)
        sys.exit(e)
    data = connection.execute("SELECT * FROM 'table' ORDER BY 'group' DESC;")
    data = data.fetchall()
    data.sort(key=operator.itemgetter(7))
    locations = connection.execute("SELECT DISTINCT location FROM 'table';")
    locations = locations.fetchall()
    locations.sort(key=operator.itemgetter(0))
    connection.close()
    return render_template("iframe.html", data=data, locations=locations)


@app.route("/device/<device_id>")
def device(device_id):
    try:
        engine = db.create_engine(f'sqlite:///{database_Env}', connect_args={'check_same_thread': False})
        connection = engine.connect()
        Session = sessionmaker(bind=engine)
        session = Session()
        print('Connected to DB')
    except Exception as e:
        print(e)
        sys.exit(e)
    data = session.query(Table).filter_by(id=f'{device_id}').first()
    connection.close()
    return render_template("device.html", data=data)


@app.route("/discover_device/<device_id>")
def discover_device(device_id):
    import subprocess
    proc = subprocess.Popen(['python3.7', 'single.py', f'{device_id}'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    proc.wait()
    return redirect(url_for('device', device_id=device_id))


@app.route("/discovery")
def discovery():
    import subprocess
    proc = subprocess.Popen(['python3.7', 'discovery.py'], stdout=subprocess.PIPE, universal_newlines=True)
    def inner():
        i = 0
        for stdout in iter(proc.stdout.readline, ""):
            if i == 0:
                i = i + 1
                yield header
            yield str(stdout) + "<br>\n"
    return Response(inner(), mimetype='text/html')


@app.route("/prune")
def prune():
    import subprocess
    proc = subprocess.Popen(['python3.7', 'prune.py'], stdout=subprocess.PIPE, universal_newlines=True)
    def inner():
        i = 0
        for stdout in iter(proc.stdout.readline, ""):
            if i == 0:
                i = i + 1
                yield header
            yield str(stdout) + "<br>\n"
    return Response(inner(), mimetype='text/html')


@app.route("/logs")
def log():
    with open('errors.log') as file:
        data = file.read()
    data = data.split('\n')
    return render_template("logs.html", data=data)


@app.route('/api/v1/modify/<getData>', methods=['GET'])
def api_modify(getData):
    #Allowed fields
    Allowed = ['computer','description','extensionAttribute2','extensionAttribute3','extensionAttribute5']
    #Split data
    requestData = convertRequest(getData)
    #Get List of Keys
    requestList = list(requestData)
    #Check if computer is specified
    if Allowed[0] not in requestData:
        result = {"result": 1, "description": "failure", "message": 'Error, no computer defined'}
    #Check if all attributes are in Allowed list
    elif len(set(requestList).difference(Allowed)) > 0:
        result = {"result": 1, "description": "failure", "message": str(set(requestList).difference(Allowed))}
    #Process request
    else:
        result = []
        search_filter = requestData['computer']
        search_filter = f'(cn={search_filter})'
        requestData.pop('computer')
        for key in requestData:
            ldap_attribute = key
            data = requestData[key]
            resultData = ldap.update(server_Env, user_name_Env, user_pass_Env, search_base_Env, search_attributes_Env ,search_filter, ldap_attribute, data)
            resultData['ldap_attribute'] = key
            resultData['data'] = data
            result.append(resultData)
    #Convert to JSON for return
    result = json.dumps(result)
    logging.info(result)
    return f'{result}'


@app.route('/api/v1/move/<getData>', methods=['GET'])
def api_move(getData):
    #Allowed fields
    AllowedKeys = ['computer','ou']
    AllowedValues = ['new','staging']
    OUs = {'new':'OU=New Computers,OU=NWMS Computers,DC=internal,DC=northwestmotorsportinc,DC=com','staging':'OU=Staging,OU=New Computers,OU=NWMS Computers,DC=internal,DC=northwestmotorsportinc,DC=com'}
    #Split data
    requestData = convertRequest(getData)
    #Get List of Keys
    requestList = list(requestData)
    #Check if computer is specified
    if AllowedKeys[0] not in requestData:
        result = {"result": 1, "description": "failure", "message": 'Error, no computer defined'}
    elif len(requestList) != 2:
        result = {"result": 1, "description": "failure", "message": 'Error, incorrect number of parameters defined'}
    #Check if all attributes are in Allowed list
    elif len(set(requestList).difference(AllowedKeys)) > 0:
        result = {"result": 1, "description": "failure", "message": f'{requestList}\n{AllowedKeys}'}
        #str(set(requestList).difference(AllowedKeys))
    #Check if OU Value is allowed
    elif requestData['ou'] not in AllowedValues:
        result = {"result": 1, "description": "failure", "message": "OUs must be 'new' or 'staging'"}
    #Process request
    else:
        result = []
        search_filter = requestData['computer']
        search_filter = f'(cn={search_filter})'
        requestData.pop('computer')
        for key in requestData:
            requestValue = requestData[key]
        new_ou = OUs[requestValue]
        resultData = ldap.move(server_Env, user_name_Env2, user_pass_Env2, search_base_Env, search_attributes_Env ,search_filter, new_ou)
        resultData['computer'] = search_filter
        resultData['data'] = new_ou
        result.append(resultData)
    #Convert to JSON for return
    result = json.dumps(result)
    logging.info(result)
    return f'{result}'


@app.route("/cron_discovery")
def cron_discovery():
    logging.info('Running /cron_dicovery')
    import subprocess
    subprocess.Popen(['python3.7', 'discovery.py'])


@app.route("/cron_prune")
def cron_prune():
    logging.info('Running /cron_prune')
    import subprocess
    subprocess.Popen(['python3.7', 'prune.py'])


sched = BackgroundScheduler(daemon=True)
sched.add_job(cron_discovery,'interval',minutes=5)
sched.add_job(cron_prune,'interval',minutes=300)
sched.start()

#if you don't want to use https or you want debugging
#if __name__ == "__main__":
#    app.run(host="0.0.0.0", debug=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", ssl_context=('../server.x509', '../server.key'))
