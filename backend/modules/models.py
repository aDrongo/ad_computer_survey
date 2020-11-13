from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from datetime import datetime
from modules.config import config

from modules.ldap import search
from modules.scanner import scan

db = SQLAlchemy()

class Devices():
    devices = []
    history = []
    locations = []
    
    def get_devices(self):
        self.devices = Device.query.all()
        return self.devices
    
    def get_devices_dict(self):
        if self.get_devices():
            return [device.to_dict() for device in self.devices]
        else:
            return []

    def get_history(self):
        self.history = History.query.all()
        return self.history

    def get_history_dict(self):
        if self.get_history():
            return [history.to_dict() for history in self.history]
        else:
            return []

    def get_locations(self):
        dynamic_locations = [row.location for row in Device.query.with_entities(Device.location).distinct().all()]
        locations_order = config['locations_order']
        for l in dynamic_locations:
            if l not in locations_order:
                locations_order.append(l)
        try:
            index = locations_order.index('unknown')
            unknown = locations_order.pop(index)
            locations_order.append(unknown)
        except ValueError:
            pass
        self.locations = locations_order
        return self.locations

    def update_devices(self):
        return [d.update() for d in self.devices]
    
    def sync_ldap(self):
        for ldap_device in search():
            found = False
            for device in self.devices:
                if device.id == ldap_device.cn.value:
                    device.import_ldap_device(ldap_device)
                    found = True
                    break
            if not (found):
                self.devices.append(Device().import_ldap_device(ldap_device))
        return self.devices

    def scan(self):
        self.devices = scan(self.devices)
        return self.devices

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

    def __init__(self, id=None):
        self.existing_device = None
        self.history = None
        if id:
            self.id = id

    def get(self):
        result = Device.query.filter_by(id=f"{self.id}").scalar()
        self._merge(result)
        return result
    
    def get_history(self):
        self.history = History.query.filter_by(device=f"{self.id}").all()
        return self.history

    def get_history_dict(self):
        self.get_history()
        return [h.to_dict() for h in self.history]

    def update(self):
        if self._check_existing():
            return self._merge_device()
        else:
            return self._add_device()

    def delete(self):
        db.session.delete(self.get())
        try:
            self._commit()
            return {'message':'success'}
        except Exception:
            return {'error'}
    
    def import_ldap_device(self, device=None):
        if device:
            self.id = device.cn.value
            self.dns = device.dNSHostName.value
            self.group = self._get_ou_group(device.distinguishedName.value)
            self.ldap = True
            self.description = device.description.value
            self.lastlogon = device.lastlogon.value
            self.os = device.operatingSystem.value
            self.version = device.operatingSystemVersion.value
            self.attribute1 = device.extensionAttribute1.value
            self.attribute2 = device.extensionAttribute2.value
            self.attribute3 = device.extensionAttribute3.value
            self.attribute4 = device.extensionAttribute4.value
            self.attribute5 = device.extensionAttribute5.value
            return self
        else:
            return None
    
    def sync_ldap(self):
        try:
            return self.import_ldap_device(search(self.id)[0])
        except Exception:
            return False
    
    def scan(self):
        result = scan([self])[0]
        self._merge(result)
        return result

    def _merge(self, item=None):
        if item:
            for key, value in item.to_dict().items():
                if value:
                    self.key = value
        return self

    def _get_ou_group(self, ou):
        import re
        group = str((re.search(r'OU=\w+\s*\w*', str(ou))).group(0)).replace("OU=","")
        return group
    
    def _check_existing(self):
        existing_device = Device.query.filter_by(id=f'{self.id}')
        if existing_device.count() > 0:
            self.existing_device = existing_device.first()
            self._check_location()
            return True
        else:
            return False
    
    def _check_location(self):
        if self.location == 'unknown' and self.existing_device.location == 'unknown':
            if (self.attribute2 and self.attribute2 != 'unknown'):
                self.location = self.attribute2
        elif self.location == 'unknown' and self.existing_device.location and self.existing_device.location != 'unknown':
                self.location = self.existing_device.location
    
    def _add_device_history(self):
        if (self.existing_device):
            keys = self._fields_changed()
            if len(keys) > 0:
                db.session.add(History(
                    device = self.id,
                    fields_changed = keys,
                    time = datetime.utcnow().strftime("%Y-%m-%d %H:%M"),
                    new_values = self.to_dict(),
                    old_values = self.existing_device.to_dict()
                ))
                return self._commit()
        else:
            db.session.add(History(
                    device = self.id,
                    fields_changed = [key for key, value in self.to_dict().items() if value != None],
                    time = datetime.utcnow().strftime("%Y-%m-%d %H:%M"),
                    new_values = self.to_dict()
                ))
            return self._commit()
    
    def _fields_changed(self):
        dict1 = self.to_dict()
        dict2 = self.existing_device.to_dict()
        results = []
        keys = dict1.keys()
        for k in keys:
            if k not in ["time_stamp","ping_time","lastup","lastlogon","os","version"]:
                if dict1[k] != dict2[k] and dict1[k] != None:
                    results.append(k)
        return results

    def _merge_device(self):
        self._add_device_history()
        db.session.merge(self)
        return self._commit()
    
    def _add_device(self):
        self._add_device_history()
        db.session.add(self)
        return self._commit()
    
    def _commit(self):
        try:
            db.session.commit()
            return self
        except Exception as e:
            db.session.rollback()
            logging.debug(e)
            return e

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