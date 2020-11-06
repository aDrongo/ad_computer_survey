from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from modules.logger import logging
from modules.config import config
from modules.scheduler import scheduler
from modules.models import db
from modules.views import views

import os

app = Flask(__name__)
#app.config.from_pyfile(config_filename)
app.config['JOBS'] = {}
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{config["database"]}'
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

db.init_app(app)
app.app_context().push()
db.create_all()

app.register_blueprint(views,url_prefix='/api')

if __name__ == "__main__":
    scheduler.start()
    if(os.environ.get('environment', None) == 'PROD'):
        print('Running in Prod')
        app.run(host="0.0.0.0", ssl_context=('./server.x509', './server.key'), use_reloader=False)
    else:
        print('Running in Dev')
        app.run(host="0.0.0.0", debug=True, use_reloader=False)
