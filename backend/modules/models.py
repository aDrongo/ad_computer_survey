from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin

db = SQLAlchemy()

class Device(db.Model, SerializerMixin):
    """Table for devices"""
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
    dns = db.Column(db.String())
    ldap = db.Column(db.Boolean())
    pass

def ldap_to_devices(ldap_devices):
    devices = []
    for device in ldap_devices:
        devices.append(Device(
            id = device.cn.value,
            dns = device.dNSHostName.value,
            group = getGroup(device.distinguishedName.value),
            ldap = True
        ))
    return devices

def getGroup(ou):
    """Use Regex to get first OU Group"""
    import re
    group = str((re.search(r'OU=\w+\s*\w*', str(ou))).group(0)).replace("OU=","")
    return group
