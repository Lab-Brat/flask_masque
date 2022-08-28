from flask import Flask
from flask_migrate import Migrate
from flask_login import LoginManager
from models import db, Users
from routes_auth import routes_auth
from routes_hosts import routes_hosts
from routes_units import routes_units
from routes_service import routes_service
from tools import DB_Tools
import os

def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DB_URI")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'd2n9WaEWR8RfMVlXzBHm'

    db.init_app(app)
    migrate = Migrate(app, db)

    login_manager = LoginManager()
    login_manager.login_view = 'routes_auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return Users.query.get(int(user_id))

    app.register_blueprint(routes_auth, url_prefix='')
    app.register_blueprint(routes_hosts, url_prefix='')
    app.register_blueprint(routes_units, url_prefix='')
    app.register_blueprint(routes_service, url_prefix='')

    # admin user
    with app.app_context():
        DB_Tools(db).admin_user()

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0')
