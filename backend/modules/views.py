from flask import Blueprint, request, jsonify, abort

from modules.logger import logging
from modules.config import config
import modules.database as Database
import modules.models as Models
import modules.ldap as Ldap
import modules.scanner as Scanner

from modules.tools import get_token,requires_auth,check_auth,calc_hash

views = Blueprint('views', __name__)

def no_object_found():
    return jsonify({"error": "No Object Found"}), 404

@views.route("/login", methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.headers.get('username')
        password = request.headers.get('password')
        if Database.check_user(username, calc_hash(password)):
            return jsonify({'token': get_token(username)})
        else:
            return jsonify({'error':'Incorrect Login'}), 401
    else:
        auth = request.headers.get('Authorization')
        if not auth:
            return jsonify({'error': 'Auth Token Required'}), 210
        if check_auth(auth):
            return jsonify({'message': 'Success'}), 200
        else:
            return jsonify({'error': 'Auth Token Incorrect'}), 210

@views.route("/users", methods=['GET', 'POST','DELETE'])
@requires_auth
def users():
    if request.method == 'POST':
        username = request.headers.get('username')
        password = request.headers.get('password')
        if username and password and username != "admin":
            return jsonify(
                Database.update_user(
                    Models.User(
                        username=username,
                        password=calc_hash(password)
                    )))
        else:
            return jsonify({'error': 'Headers not provided'}), 404
    elif request.method == 'DELETE':
        username = request.headers.get('username')
        if username and username != "admin":
            return jsonify(
                Database.delete_user(
                    Models.User(
                        username=username
                    )))
        else:
            return jsonify({'error': 'Headers not provided'}), 404
    else:
        users = []
        [users.append(u.username) for u in Database.get_users() if u.username != "admin"]
        return jsonify(users)

@views.route("/devices")
def devices():
    return jsonify([device.to_dict() for device in Database.get_devices()])

@views.route("/device/<id>", methods=['GET', 'POST','DELETE'])
@requires_auth
def device(id):
    if request.method == 'POST':
        return jsonify(Database.update_device(Models.Device(id=id)))
    elif request.method == 'DELETE':
        return jsonify(Database.delete_device(Database.get_device(id)))
    else:
        device = Database.get_device(id)
        return jsonify(device.to_dict()) if device else no_object_found()

@views.route("/locations")
def locations():
    return jsonify(Database.get_locations())

@views.route("/scan")
def scans():
    try:
        ldap_devices = Ldap.search()
        Database.sync_ldap_devices(ldap_devices)
    except Exception as e:
        pass
    devices = Database.get_devices()
    results = Scanner.scan(devices)
    [Database.update_device(r) for r in results]
    return jsonify([device.to_dict() for device in results])

@views.route("/scan/<id>")
def scan(id):
    try:
        ldap_devices = Ldap.search(id)
        Database.sync_ldap_devices(ldap_devices)
    except Exception as e:
        pass
    device = Database.get_device(id)
    if device == None:
        return no_object_found()
    else:
        results = Scanner.scan([device])
        [Database.update_device(r) for r in results]
        return jsonify([device.to_dict() for device in results])

@views.route("/configuration", methods=['GET', 'POST'])
@requires_auth
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

@views.route("/logs/plain")
@requires_auth
def logs_plain():
    with open('errors.log', 'r') as f:
        data = f.read()
    return data.replace('\n','<br>')

@views.route("/logs/json")
@requires_auth
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