import time

import modules.models as Models

from modules.logging import logging
from modules.config import config

def check_user(username,password):
    user = Models.User.query.filter_by(username=f"{username}")
    if user.count() == 0:
        return False
    else:
        return password == user.first().password

def get_users():
    return Models.User.query.all()

def update_user(user):
    existing_user = Models.User.query.filter_by(username=f'{user.username}')
    if existing_user.count() > 0:
        Models.db.session.merge(user)
        try:
            Models.db.session.commit()
        except:
            Models.db.session.rollback()
            return False
    else:
        Models.db.session.add(user)
        try:
            Models.db.session.commit()
        except:
            Models.db.session.rollback()
            return False
    return True

def delete_user(user):
    existing_user = Models.User.query.filter_by(username=f'{user.username}').scalar()
    if existing_user:
        Models.db.session.delete(existing_user)
        try:
            Models.db.session.commit()
        except Exception as e:
            Models.db.session.rollback()
            return {"Error":e}
        return {"Success":f"Deleted user {user.username}"}
    return {"Error":"User not found"}

def get_devices():
    return Models.Device.query.all()

def get_device(id):
    return Models.Device.query.filter_by(id=f"{id}").first()

def get_locations():
    dynamic_locations = [row.location for row in Models.Device.query.with_entities(Models.Device.location).distinct().all()]
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
    return locations_order

def update_device(device):
    """Will Insert or Update Database with Device"""
    existing_device = Models.Device.query.filter_by(id=f'{device.id}')
    if existing_device.count() > 0:
        if device.location == 'unknown':
            if (device.attribute2 and device.attribute2 != 'unknown'):
                device.location = device.attribute2
            else:
                device.location = existing_device.first().location
        Models.db.session.merge(device)
        try:
            Models.db.session.commit()
        except:
            Models.db.session.rollback()
            return False
    else:
        Models.db.session.add(device)
        try:
            Models.db.session.commit()
        except:
            Models.db.session.rollback()
            return False
    return True

def delete_device(device):
    if device == None:
        return {"Error":"No device submited"}
    Models.db.session.delete(device)
    try:
        Models.db.session.commit()
    except Exception as e:
        Models.db.session.rollback()
        return {"Error":e}
    return {"Success":f"Deleted device {device.id}"}

def sync_ldap_devices(ldap_devices):
    devices = Models.ldap_to_devices(ldap_devices)
    for device in devices:
        update_device(device)
    pass