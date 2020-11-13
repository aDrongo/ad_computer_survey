from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from modules.logger import logging

def create_app():
    app = Flask(__name__)
    return app

class AppInitializer:
    def __init__(self):
        self.app = create_app()

    def load_configuration(self):
        from modules.config import config
        self.config = config

    def set_configuration(self):
        self.app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    def db_path(self,path):
         self.app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{path}'

    def db_init(self):
        from modules.models import db
        db.init_app(self.app)
    
    def db_push(self):
        from modules.models import db
        self.app.app_context().push()
    
    def db_create(self):
        from modules.models import db
        db.create_all()
    
    def db_setup(self):
        self.db_path(self.config["database"])
        self.db_init()
        self.db_push()
        self.db_create()

    def db_teardown(self):
        self.app.app_context().pop()

    def set_cors(self):
        CORS(self.app)

    def register_views(self):
        from modules.views import views
        self.app.register_blueprint(views,url_prefix='/api')

    def configure_schedule(self):
        import modules.scheduler as Scheduler
        Scheduler.add_cron_scan(self.config['scan_schedule'])
        Scheduler.scheduler.start()

    def configure_admin(self,password):
        import modules.database as Database
        import modules.models as Models
        from modules.tools import calc_hash
        Database.update_user((Models.User(username='admin',password=calc_hash(password))))

    def setup(self):
        self.load_configuration()
        self.set_configuration()
        self.set_cors()
        self.db_setup()
        self.register_views()
        self.configure_schedule()
        self.configure_admin(self.config['admin_password'])

    def run(self):
        self.app.run(host="0.0.0.0", debug=True, use_reloader=False)
    
    def get_app(self):
        return self.app

if __name__ == "__main__":
    app = AppInitializer()
    app.run()

