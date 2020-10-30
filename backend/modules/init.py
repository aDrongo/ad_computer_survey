from flask import Flask

from modules.logging import logging
from modules.config import config

import modules.database as Database
import modules.models as Models


app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{config["database"]}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

from modules.models import db
db.init_app(app)
app.app_context().push()
db.create_all()

Database.update_user((Models.User(username='admin',password=hash(config['admin_password']))))