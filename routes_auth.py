from flask import Blueprint
from flask import render_template, redirect, flash, url_for, session
from flask_login import login_user, login_required, logout_user, current_user
from flask import request
from models import db, Users, ActiveSessions
from tools import DB_Tools
import uuid

DBT = DB_Tools(db)
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
        uid = str(uuid.uuid4())
        DBT.session_add(uid)
        session_info = ActiveSessions.query.filter_by(uuid=uid).all()[0]
        session['id'] = session_info.id
        session['uuid'] = session_info.uuid
        return render_template('profile.html', 
                               name = current_user.name,
                               email = current_user.email)
    else:
        return render_template('login.html')

@routes_auth.route('/logout')
@login_required
def logout():
    DBT.session_delete(session['id'])
    logout_user()
    return 'User Logged Out!'

@routes_auth.route('/profile')
@login_required
def profile():
    return render_template('profile.html', 
                           name = current_user.name,
                           email = current_user.email)
