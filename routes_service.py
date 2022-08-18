from flask import Blueprint
from flask import request, render_template
from models import db
from tools import Tools, DB_Tools


T = Tools()
DBT = DB_Tools(db)
routes_service = Blueprint("routes_service", __name__)

@routes_service.route('/search', methods = ['GET', 'POST'])
def search():
    if request.method == "POST":
        query = request.form['query']
        result = [h for h in DBT.host_query() if query in h]
        host_dict = DBT.get_form_dict()
        forms = [host_dict[r] for r in result]
        return render_template('search.html', forms = forms)
    return render_template('search.html')
