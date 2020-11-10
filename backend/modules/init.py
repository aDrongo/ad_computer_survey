from modules.config import config
from modules.tools import calc_hash
from modules.logger import logging

import modules.database as Database
import modules.models as Models
import modules.scheduler as Scheduler

def init():
    Scheduler.add_cron_scan(config['scan_schedule'])
    Scheduler.scheduler.start()
    Database.update_user((Models.User(username='admin',password=calc_hash(config['admin_password']))))