from flask import Blueprint
from flask import render_template
from models import db

routes_auth = Blueprint('auth', __name__)


@routes_auth.route('/login')
def login():
    return render_template('login.html')

@routes_auth.route('/logout')
def logout():
    return 'Logout'
