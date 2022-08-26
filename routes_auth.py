from flask import Blueprint
from flask import render_template, redirect
from flask import request
from models import db

routes_auth = Blueprint('routes_auth', __name__)


@routes_auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        redirect('/profile')
    else:
        return render_template('login.html')

@routes_auth.route('/logout')
def logout():
    return 'Logout'

@routes_auth.route('/profile')
def profile():
    return 'Profile'
