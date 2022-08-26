from flask import Blueprint
from flask import render_template, redirect, flash, url_for
from flask_login import login_user
from flask import request
from models import db, Users

routes_auth = Blueprint('routes_auth', __name__)


@routes_auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False

        user = Users.query.filter_by(email=email).first()

        if not user or not user.password == password:
            flash('Please check your login details and try again.')
            return redirect(url_for('routes_auth.login'))

        login_user(user, remember=remember)
        # return render_template('profile.html')
        return 'Authenticated!'
    else:
        return render_template('login.html')

@routes_auth.route('/logout')
def logout():
    return 'Logout'

@routes_auth.route('/profile')
def profile():
    return 'Profile'
