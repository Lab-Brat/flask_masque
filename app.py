from flask import Flask, request
from flask import redirect, render_template, send_file
from flask_migrate import Migrate
from models import db, CreateForm, CreateExIP, CreateUnits
from tools import Tools, DB_Tools
import os
import csv
import json


# ------------------------------ Load Configs ------------------------------- #
app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DB_URI")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'topsecretkey'

dirlist = ['RedHat', 'Debian', 'Arch', 'SUSE', 'Gentoo', 'BSD']

db.init_app(app)
migrate = Migrate(app, db)

# ------------------------------- Main Routes ------------------------------- #
# open new form input page after pressing "Add Form"
@app.route('/form', methods=['POST', 'GET'])
def form():
    if request.method == 'POST':
        new_form = CreateForm(
                name=request.form['name'],
                hostname=request.form['hostname'],
                unit_belong=request.form['unit_belong'],
                ip=request.form['ip'],
                distro=request.form['distro'],
                functions=request.form['functions'],
                subsystems=request.form['subsystems'])

        if new_form.hostname in DB_Tools(db).host_query():
            return ('HOSTNAME EXISTS!!!\n'
                    'Next time please click on "Check Hostname"'
                    'button before filling out the whole form!')

        db.session.add(new_form)
        db.session.flush()

        extra_ip = request.form.getlist('field[]')
        new_extra_ips = [CreateExIP(forms_id=new_form.id, 
                                    extra_ip=ip) for ip in extra_ip]
        db.session.add_all(new_extra_ips)
        db.session.commit()
        return redirect('/')

    else:
        return render_template('form.html',
                            dirlist=dirlist, 
                            units=DB_Tools(db).unit_query(),
                            hosts=json.dumps(DB_Tools(db).host_query()),
                            unit_data=json.dumps(DB_Tools(db).data_query()))

# delete form after pressing "Delete" link
@app.route('/delete/<int:id>')
def delete(id):
    form_to_delete = CreateForm.query.get_or_404(id)

    try:
        db.session.delete(form_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return "Failed to Delete Form"

# open update page after pressing "Update" link
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    form = CreateForm.query.get_or_404(id)

    if request.method == 'POST':
        form.name=request.form['name']
        form.hostname=request.form['hostname']
        form.unit_belong=request.form['unit_belong'],
        form.ip=request.form['ip']
        form.distro=request.form['distro']
        form.functions=request.form['functions']
        form.subsystems=request.form['subsystems']

        # change existring extra IPs
        exip_form = request.form.getlist('extra_ips[]')
        exip_db = [ip for ip in DB_Tools(db).extra_ip_query()
                             if ip.forms_id == id]
        for i, ip in enumerate(exip_form):
            exip_db[i].extra_ip = ip

        # process newly created extra IPs
        extra_ip = request.form.getlist('field[]')
        new_extra_ips = [CreateExIP(forms_id=form.id, 
                                    extra_ip=ip) for ip in extra_ip]

        db.session.add_all(new_extra_ips)

        try:
            db.session.commit()
            return redirect('/')
        except:
            return "Failed to Update Form"
    else:
        return render_template('update.html', form=form, dirlist=dirlist, 
                            units=DB_Tools(db).unit_query(),
                            hosts=json.dumps(DB_Tools(db).host_query()),
                            unit_data=json.dumps(DB_Tools(db).data_query()))

# Save all database data into csv file
@app.route('/dump', methods=['GET'])
def dump():
    exip_dict = {}
    for instance in DB_Tools(db).extra_ip_query():
        if str(instance.forms_id) in exip_dict:
            exip_dict[str(instance.forms_id)] += '\r\n' + instance.extra_ip
        else:
            exip_dict[str(instance.forms_id)] = instance.extra_ip
    
    dump_file = f'./dumps/dump_{Tools().timestamp()}.csv'
    os.makedirs(os.path.dirname(dump_file), exist_ok=True)

    header = ['Name', 'Hostname', 'Org. Unit', 'IP', 
              'Extra IPs', 'Functions', 'Subsystems']

    with open(dump_file, 'w', encoding='UTF8') as dump:
        writer = csv.writer(dump)
        writer.writerow(header)
        for instance in DB_Tools(db).get_model('form'):
            try:
                exip_csv = exip_dict[str(instance.id)]
            except:
                exip_csv = ''
            row_data = [instance.name, instance.hostname, 
                        instance.unit_belong, 
                        instance.ip, exip_csv,
                        instance.functions, instance.subsystems]
            writer.writerow(row_data)

    return send_file(dump_file, mimetype='text/csv', 
                     download_name='db_dump.csv')

# main page
@app.route('/', methods=['GET', 'POST'])
def index():
    forms = DB_Tools(db).get_model('form')
    return render_template('index.html', forms=forms)


# ---------------------------- Org. Unit Routes ----------------------------- #
@app.route('/unit_new', methods=['POST', 'GET'])
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

@app.route('/unit_update/<int:id>', methods=['POST', 'GET'])
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

@app.route('/unit_delete/<int:id>', methods=['POST', 'GET'])
def unit_delete(id):
    unit_to_delete = CreateUnits.query.get_or_404(id)

    for h in DB_Tools(db).model_query('form'):
        if h.unit_belong == unit_to_delete.unit_name:
            h.unit_belong = None

    db.session.delete(unit_to_delete)
    db.session.commit()
    return redirect('/unit')

@app.route('/unit_dump', methods=['GET'])
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

@app.route('/unit', methods=['POST', 'GET'])
def unit():
    hosts = DB_Tools(db).host_unit_query()

    hc = {cl.unit_name: [] for cl in DB_Tools(db).get_model('unit')}
    [hc[h[1]].append(h[0]) for h in hosts if h[1] in hc.keys()]

    return render_template('unit.html', hc_dict=hc, 
                           units=DB_Tools(db).get_model('unit'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

