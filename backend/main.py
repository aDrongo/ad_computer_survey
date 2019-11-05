from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from apscheduler.schedulers.background import BackgroundScheduler

from modules.views import views

import os
import logging
import logging.handlers

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s', 
    handlers=[logging.handlers.RotatingFileHandler("errors.log", maxBytes=1000000, backupCount=3)])

app = Flask(__name__)
#app.config.from_pyfile(config_filename)
import modules.config as Config
config = Config.load()
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{config["database"]}'
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

from modules.models import db
db.init_app(app)
app.app_context().push()
db.create_all()

app.register_blueprint(views)

#sched = BackgroundScheduler(daemon=True)
#sched.add_job(cron_scan,'interval',minutes=5)
#sched.start()

if __name__ == "__main__":
    if(os.environ.get('environment', None) == 'prod'):
        print('Running in Prod')
        app.run(host="0.0.0.0", ssl_context=('../server.x509', '../server.key'), use_reloader=False)
    else:
        print('Running in Dev')
        app.run(host="0.0.0.0", debug=True, use_reloader=False)
