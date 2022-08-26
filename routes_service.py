from flask import Blueprint
from flask import request, render_template
from models import db
from tools import Tools, DB_Tools


T = Tools()
DBT = DB_Tools(db)
routes_service = Blueprint("routes_service", __name__)
