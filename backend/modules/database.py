import modules.models as Models
import modules.config as Config
import time

config = Config.load()

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
