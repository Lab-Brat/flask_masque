from flask import Flask
from flask_migrate import Migrate
from models import db
from routes_hosts import routes_hosts
from routes_units import routes_units
import os

# ------------------------------ Load Configs ------------------------------- #
app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DB_URI")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'topsecretkey'

db.init_app(app)
migrate = Migrate(app, db)

# ------------------------------- App Routes -------------------------------- #
app.register_blueprint(routes_hosts, url_prefix='')
app.register_blueprint(routes_units, url_prefix='')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

