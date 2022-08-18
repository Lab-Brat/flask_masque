from flask import Blueprint
from flask import request, render_template, redirect
from models import db, CreateForm, CreateExIP
from tools import Tools, DB_Tools


T = Tools()
DBT = DB_Tools(db)
routes_service = Blueprint("routes_service", __name__)

@routes_service.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == "POST":
        data = ['Your search bar WORKS!']
        return render_template('search.html', data=data)
    return render_template('search.html')
