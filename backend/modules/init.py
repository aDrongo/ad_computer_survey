from modules.config import config
from modules.tools import calc_hash
from modules.scheduler import scheduler

import modules.database as Database

def init():
    scheduler.start()
    Database.update_user((Models.User(username='admin',password=calc_hash(config['admin_password']))))