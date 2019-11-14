from flask import Flask, render_template, Response, redirect, url_for
import sqlalchemy as db
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
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

logging.basicConfig(filename=f'errors.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Load Config
try:
    with open('config.json') as f:
        config = json.loads(f.read())
    try:
        database_EnvVariable = str(config['database_EnvVariable'])
    except Exception as e:
        logging.debug(e)
        sys.exit('Config file incorrect')
except Exception as e:
    logging.debug(e)
    sys.exit('Config file not loaded')

header = """
<!DOCTYPE html>
<html>
 <head>
  <meta charset="utf-8" http-equiv="refresh" content="60" >
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


def rename(var):
    if var == 0:
        return 'good'
    else:
        return 'bad'


app = Flask(__name__)


@app.route("/")
def home():
    try:
        engine = db.create_engine(f'sqlite:///{database_EnvVariable}', connect_args={'check_same_thread': False})
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
        engine = db.create_engine(f'sqlite:///{database_EnvVariable}', connect_args={'check_same_thread': False})
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
        engine = db.create_engine(f'sqlite:///{database_EnvVariable}', connect_args={'check_same_thread': False})
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



@app.route("/cron_discovery")
def cron_discovery():
    import subprocess
    subprocess.Popen(['python3.7', 'discovery.py'])


@app.route("/cron_prune")
def cron_prune():
    import subprocess
    subprocess.Popen(['python3.7', 'prune.py'])


sched = BackgroundScheduler(daemon=True)
sched.add_job(cron_discovery,'interval',minutes=10)
sched.add_job(cron_prune,'interval',minutes=300)
sched.start()

# if you don't want to use https or you want debugging
# if __name__ == "__main__":
#    app.run(host="0.0.0.0", debug=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", ssl_context=('../server.x509', '../server.key'))
