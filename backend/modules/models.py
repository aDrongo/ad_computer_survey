from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin

db = SQLAlchemy()

class Device(db.Model, SerializerMixin):
    """Table for devices"""
    __tablename__ = 'devices'
    id = db.Column(db.String(), primary_key=True)
    ip = db.Column(db.String())
    ping_code = db.Column(db.Integer())
    ping_time = db.Column(db.Float())
    time_stamp = db.Column(db.String())
    description = db.Column(db.String())
    attribute1 = db.Column(db.String())
    attribute2 = db.Column(db.String())
    attribute3 = db.Column(db.String())
    attribute4 = db.Column(db.String())
    attribute5 = db.Column(db.String())
    location = db.Column(db.String())
    group = db.Column(db.String())
    lastup = db.Column(db.String())
    lastlogon = db.Column(db.String())
    os = db.Column(db.String())
    version = db.Column(db.String())
    dns = db.Column(db.String())
    ldap = db.Column(db.Boolean())

class User(db.Model, SerializerMixin):
    """Table for devices"""
    __tablename__ = 'users'
    username = db.Column(db.String(), unique=True, primary_key=True)
    password = db.Column(db.String())

class History(db.Model, SerializerMixin):
    """Table for history of changes"""
    __tablename__ = 'history'
    id = db.Column(db.Integer(), unique=True, primary_key=True)
    device = db.Column(db.String())
    time = db.Column(db.String())
    fields_changed = db.Column(db.PickleType())
    new_values = db.Column(db.PickleType())
    old_values = db.Column(db.PickleType())

def ldap_to_devices(ldap_devices):
    devices = []
    for device in ldap_devices:
        devices.append(Device(
            id = device.cn.value,
            dns = device.dNSHostName.value,
            group = getGroup(device.distinguishedName.value),
            ldap = True,
            description = device.description.value,
            lastlogon = device.lastlogon.value,
            os = device.operatingSystem.value,
            version = device.operatingSystemVersion.value,
            attribute1 = device.extensionAttribute1.value,
            attribute2 = device.extensionAttribute2.value,
            attribute3 = device.extensionAttribute3.value,
            attribute4 = device.extensionAttribute4.value,
            attribute5 = device.extensionAttribute5.value
        ))
    return devices

def getGroup(ou):
    """Use Regex to get first OU Group"""
    import re
    group = str((re.search(r'OU=\w+\s*\w*', str(ou))).group(0)).replace("OU=","")
    return group
