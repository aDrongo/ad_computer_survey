from flask import Flask, Response, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from apscheduler.schedulers.background import BackgroundScheduler
from multiprocessing import Process
from functools import wraps

import requests
import os
import json
import logging
import logging.handlers

import modules.config as Config
import modules.database as Database
import modules.models as Models
import modules.ldap as Ldap
import modules.scanner as Scanner

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s', 
    handlers=[logging.handlers.RotatingFileHandler("errors.log", maxBytes=1000000, backupCount=3)])

config = Config.load()
app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{config["database"]}'
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
Models.db.init_app(app)
app.app_context().push()
Models.db.create_all()


def require_appkey(view_function):
    @wraps(view_function)
    def decorated_function(*args, **kwargs):
        return view_function(*args, **kwargs) if check_request_key(request) else abort(403)
    return decorated_function

def check_request_key(request):
    return request.headers.get('key') and request.headers.get('key') in config['AppKeys']

def no_device_found():
    return jsonify(404, "No Device Found")

@app.route("/api/devices")
def devices():
    return jsonify([device.to_dict() for device in Database.get_devices()])

@app.route("/api/device/<id>", methods=['GET', 'POST','DELETE'])
def device(id):
    logging.info(request)
    if request.method == 'POST':
        return jsonify(Database.update_device(Models.Device(id=id)))# if check_request_key(request) else abort(403)
    elif request.method == 'DELETE':
        return jsonify(Database.delete_device(Database.get_device(id)))# if check_request_key(request) else abort(403)
    else:
        device = Database.get_device(id)
        return jsonify(device.to_dict()) if device else no_device_found()

@app.route("/api/locations")
def locations():
    return jsonify(Database.get_locations())

@app.route("/api/scan")
def scans():
    try:
        ldap_devices = Ldap.search()
        Database.sync_ldap_devices(ldap_devices)
    except Exception as e:
        logging.info(e)
        pass
    devices = Database.get_devices()
    results = Scanner.scan(devices)
    [Database.update_device(r) for r in results]
    return jsonify([device.to_dict() for device in results])

@app.route("/api/scan/<id>")
def scan(id):
    try:
        ldap_devices = Ldap.search(id)
        Database.sync_ldap_devices(ldap_devices)
    except Exception as e:
        logging.info(e)
        pass
    device = Database.get_device(id)
    if device == None:
        return no_device_found()
    else:
        results = Scanner.scan([device])
        [Database.update_device(r) for r in results]
        return jsonify([device.to_dict() for device in results])

@app.route("/api/configuration", methods=['GET', 'POST'])
@require_appkey
def configuration():
    if request.method == 'POST':
        with open("config.json.backup", "w") as backup:
            backup.write(json.dumps(config, indent=4, sort_keys=True))
        config.update(request.form)
        with open("config.json", "w") as new_config:
            new_config.write(json.dumps(config, indent=4, sort_keys=True))
        return jsonify(config)
    else:
        return jsonify(config)

@app.route("/api/logs/plain") #@require_appkey
def logs_plain():
    with open('errors.log', 'r') as f:
        data = f.read()
    return data.replace('\n','<br>')

@app.route("/api/logs/json") #@require_appkey
def logs_json():
    data = []
    with open('errors.log', 'r') as f:
        for l in f:
            line = l.strip().split(" ")
            obj = {
                "time": ' '.join(line[0:2]),
                "level": ' '.join(line[2:5]),
                "message": ' '.join(line[5:])
            }
            data.append(obj)
    return jsonify(data)

@app.route("/cron_scan")
def cron_scan():
    return requests.get('http://localhost:5000/api/scan').content

if __name__ == "__main__":
    sched = BackgroundScheduler(daemon=True)
    sched.add_job(cron_scan,'interval',minutes=5)
    sched.start()
    app.run(host="0.0.0.0", debug=True, use_reloader=False)