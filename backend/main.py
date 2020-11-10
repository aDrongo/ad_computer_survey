from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from modules.logger import logging
from modules.config import config
from modules.models import db
from modules.views import views
from modules.init import init

import os

app = Flask(__name__)
#app.config.from_pyfile(config_filename)
app.config['JOBS'] = {}
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{config["database"]}'
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
CORS_ALWAYS_SEND

db.init_app(app)
app.app_context().push()
db.create_all()

app.register_blueprint(views,url_prefix='/api')

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, use_reloader=False)
