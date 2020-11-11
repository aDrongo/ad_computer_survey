from flask import request, jsonify
from functools import wraps
import datetime

import hashlib
import jwt

from modules.config import config

def calc_hash(string):
    return hashlib.sha256(string.encode()).hexdigest()

def get_token(username):
    return jwt.encode(
        {
            'username': username, 
            'exp': (datetime.datetime.utcnow() + datetime.timedelta(days=1))
        },
        config['secret_key'],
        algorithm='HS256').decode('utf-8')

def check_auth(token):
    try:
        jwt.decode(token, config['secret_key'], algorithms='HS256')
        return True
    except:
        return False
    return False

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.headers.get('Authorization')
        if not auth or not check_auth(auth):
            return jsonify({'error': 'Auth Required'}), 401
        return f(*args, **kwargs)
    return decorated