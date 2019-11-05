from flask import Flask, render_template, Response, redirect, url_for
import sqlalchemy as db
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from collections import Counter
from jinja2 import Template
from apscheduler.schedulers.background import BackgroundScheduler
import os
import operator
import sys
import time
import math

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


def rename(var):
    if var == 0:
        return 'good'
    else:
        return 'bad'




app = Flask(__name__)


@app.route("/")
def home():
    db_env = 'database.sqlite'
    try:
        engine = db.create_engine(f'sqlite:///./{db_env}')
        connection = engine.connect()
        metadata = db.MetaData(bind=connection, reflect=True)
        Session = sessionmaker(bind=engine)
        session = Session()
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
    close = connection.close()
    return render_template("home.html", data=data, locations=locations)


@app.route("/device/<device_id>")
def device(device_id):
    db_env = 'database.sqlite'
    try:
        engine = db.create_engine(f'sqlite:///./{db_env}')
        connection = engine.connect()
        metadata = db.MetaData(bind=connection, reflect=True)
        Session = sessionmaker(bind=engine)
        session = Session()
        print('Connected to DB')
    except Exception as e:
        print(e)
        sys.exit(e)
    # data = connection.execute(f"SELECT * FROM 'table' WHERE 'id' = '{device_id}';")
    data = session.query(Table).filter_by(id=f'{device_id}').first()
    # data = data.fetchall()
    connection.close()
    return render_template("device.html", data=data)


@app.route("/discover_device/<device_id>")
def discover_device(device_id):
    import subprocess
    proc = subprocess.Popen(['python3', 'single.py', f'{device_id}'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    proc.wait()
    return redirect(url_for('device', device_id=device_id))


@app.route("/discovery")
def discovery():
    import subprocess
    proc = subprocess.Popen(['python3', 'discovery.py'], stdout=subprocess.PIPE, universal_newlines=True)
    header = """
<html>
<body>
    <div class="topnav">
        <a href="/">Home</a>
    </div>
"""
    def inner():
        i = 0
        for stdout in iter(proc.stdout.readline, ""):
            if i == 0:
                i = i + 1
                yield header
            yield str(stdout) + "<br>\n"
    return Response(inner(), mimetype='text/html')


@app.route("/cron_discovery")
def cron_discovery():
    import subprocess
    proc = subprocess.Popen(['python3', 'discovery.py'])


sched = BackgroundScheduler(daemon=True)
sched.add_job(cron_discovery,'interval',minutes=10)
sched.start()


if __name__ == "__main__":
    app.run(debug=True)
