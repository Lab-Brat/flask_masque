from flask import Blueprint
from flask import request, render_template, redirect, send_file
from models import db, CreateUnits
from tools import Tools, DB_Tools
import os
import csv


dirlist = Tools().dirlist
routes_units = Blueprint("routes_units", __name__)

# open form to register organizational unit information
@routes_units.route('/unit_new', methods=['POST', 'GET'])
def unit_new():
    clusters, containerizations, pods = DB_Tools(db).unit_details_query()

    if request.method == 'POST':
        new_unit = CreateUnits(
                        unit_name=request.form['unit_name'],
                        unit_level=request.form['unit_level'],
                        description=request.form['description'],
                        cluster=request.form['cluster'],
                        containerization=request.form['containerization'],
                        pod=request.form['pod'],
                        unit_functions=request.form['unit_functions'],
                        unit_subsystems=request.form['unit_subsystems'])

        db.session.add(new_unit)
        db.session.commit()

        return redirect('/unit')
    else:
        return render_template('unit_new.html', 
                               clusters=clusters, 
                               containerizations=containerizations,
                               pods=pods) 

#delete unit after pressing "Delete" link
@routes_units.route('/unit_delete/<int:id>', methods=['POST', 'GET'])
def unit_delete(id):
    unit_to_delete = CreateUnits.query.get_or_404(id)

    for h in DB_Tools(db).model_query('form'):
        if h.unit_belong == unit_to_delete.unit_name:
            h.unit_belong = None

    db.session.delete(unit_to_delete)
    db.session.commit()
    return redirect('/unit')

# open update page after pressing "Update" link
@routes_units.route('/unit_update/<int:id>', methods=['POST', 'GET'])
def unit_update(id):
    unit = CreateUnits.query.get_or_404(id)

    if request.method == 'POST':
        for h in DB_Tools(db).model_query('form'):
            if h.unit_belong == unit.unit_name:
                h.unit_belong = request.form['unit_name']
                h.functions = request.form['unit_functions']
                h.subsystems = request.form['unit_subsystems']
        
        unit.unit_name = request.form['unit_name']
        unit.unit_level = request.form['unit_level']
        unit.cluster = request.form['cluster']
        unit.containerization = request.form['containerization']
        unit.pod = request.form['pod']
        unit.description = request.form['description']
        unit.unit_functions = request.form['unit_functions']
        unit.unit_subsystems = request.form['unit_subsystems']

        db.session.commit()

        return redirect('/unit')
    else:
        return render_template('unit_update.html', unit=unit)  

# Save and download all unit records into csv file
@routes_units.route('/unit_dump', methods=['GET'])
def unit_dump():
    header = ['Name', 'Level', 'Description', 'Level Details',
              'Functions', 'Subsystems']

    dump_file = f'./dumps/dump_{Tools().timestamp()}.csv'
    os.makedirs(os.path.dirname(dump_file), exist_ok=True)

    with open(dump_file, 'w', encoding='UTF8') as dump:
        writer = csv.writer(dump)
        writer.writerow(header)
        for instance in DB_Tools(db).get_model('unit'):
            row_data = [instance.unit_name, instance.unit_level, 
                        instance.description, 
                        (f"{instance.cluster} / "
                         f"{instance.containerization} /" 
                         f"{instance.pod}"),
                         instance.unit_functions, instance.unit_subsystems]
            writer.writerow(row_data)
    
    return send_file(dump_file, mimetype='text/csv', 
                     download_name='db_dump_units.csv')

# units infromation page
@routes_units.route('/unit', methods=['POST', 'GET'])
def unit():
    hosts = DB_Tools(db).host_unit_query()

    hc = {cl.unit_name: [] for cl in DB_Tools(db).get_model('unit')}
    [hc[h[1]].append(h[0]) for h in hosts if h[1] in hc.keys()]

    return render_template('unit.html', hc_dict=hc, 
                           units=DB_Tools(db).get_model('unit'))