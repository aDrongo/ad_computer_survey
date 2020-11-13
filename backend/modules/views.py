from flask import Blueprint, request, jsonify, abort

from modules.logger import logging
from modules.config import config
import modules.database as Database
import modules.models as Models
import modules.ldap as Ldap
import modules.scanner as Scanner

from modules.tools import get_token,requires_auth,check_auth,calc_hash,no_object_found

views = Blueprint('views', __name__)

@views.route("/login", methods=['GET','POST'])
def login():
    """If Post, Login User. If Get, check if user is authorized"""
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
    """Get, Post and Delete Users"""
    if request.method == 'POST':
        username = request.headers.get('username')
        password = request.headers.get('password')
        if username == "admin":
            return jsonify({'error': 'Can not modify admin'}), 404
        elif username and password:
            return jsonify(
                Database.update_user(
                    Models.User(
                        username=username,
                        password=calc_hash(password))))
        else:
            return jsonify({'error': 'Headers not provided'}), 404
    elif request.method == 'DELETE':
        username = request.headers.get('username')
        if username == "admin":
            return jsonify({'error': 'Can not modify admin'}), 404
        elif username:
            return jsonify(
                Database.delete_user(
                    Models.User(
                        username=username)))
        else:
            return jsonify({'error': 'Headers not provided'}), 404
    else:
        users = []
        [users.append(u.username) for u in Database.get_users() if u.username != "admin"]
        return jsonify(users)

@views.route("/devices")
def devices():
    """Get Devices"""
    return jsonify(Models.Devices().get_devices_dict())

@views.route("/device/<id>", methods=['GET', 'POST','DELETE'])
@requires_auth
def device(id):
    """Get, Post and Delete a Device"""
    device = Models.Device(id=id)
    if request.method == 'POST':
        device.scan()
        device.sync_ldap()
        device.update()
        return jsonify(device.to_dict())
    device.get()
    if request.method == 'DELETE':
        return jsonify(device.delete()) if device else no_object_found()
    else:
        return jsonify(device.to_dict()) if device else no_object_found()

@views.route("/locations")
def locations():
    """Get Locations"""
    return jsonify(Models.Devices().get_locations())

@views.route("/scan")
def scans():
    devices = Models.Devices()
    devices.get_devices()
    devices.sync_ldap()
    devices.scan()
    devices.update_devices()
    return jsonify(devices.get_devices_dict())

@views.route("/scan/<id>")
def scan(id):
    device = Models.Device(id=id)
    if device.get() == None:
        return no_object_found()
    else:
        device.sync_ldap()
        device.scan()
        device.update()
        return jsonify(device.to_dict())

@views.route("/history")
def history():
    history = Models.Devices().get_history_dict()
    return jsonify(history)

@views.route("/history/<id>")
def device_history(id):
    history = Models.Device(id=id).get_history_dict()
    if history:
        return jsonify(history) if history else no_object_found()
    else:
        return no_object_found()