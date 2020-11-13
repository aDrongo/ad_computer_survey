import time

import modules.models as Models

from datetime import datetime
from modules.logger import logging
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
            return user.to_dict()
        except:
            Models.db.session.rollback()
            return {"error":e}
    else:
        Models.db.session.add(user)
        try:
            Models.db.session.commit()
            return user.to_dict()
        except:
            Models.db.session.rollback()
            return {"error":e}

def delete_user(user):
    existing_user = Models.User.query.filter_by(username=f'{user.username}').scalar()
    if existing_user:
        Models.db.session.delete(existing_user)
        try:
            Models.db.session.commit()
        except Exception as e:
            Models.db.session.rollback()
            return {"error":e}
        return {"message":f"Deleted user {user.username}"}
    else:
        return {"error":"User not found"}
