from apscheduler.schedulers.background import BackgroundScheduler
import requests

from modules.logger import logging
from modules.config import config

scheduler = BackgroundScheduler()

def cron_scan():
    requests.get('http://127.0.0.1:5000/api/scan')
    pass

def add_cron_scan(time):
    scheduler.add_job(func=cron_scan,trigger="interval", seconds=int(time))
