from flask import Blueprint
from models import db

routes_auth = Blueprint('auth', __name__)


@routes_auth.route('/login')
def login():
    return 'Login'

@routes_auth.route('/logout')
def logout():
    return 'Logout'
