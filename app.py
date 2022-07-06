from flask import Flask
from flask import request, redirect, render_template, send_file
from flask_migrate import Migrate
from models import db, CreateForm, CreateExIP, CreateUnits
from tools import Tools
from datetime import datetime
import configparser
import csv
import json


# ------------------------------ Load Configs ------------------------------- #
config = configparser.ConfigParser()
config.read_file(open('config.ini'))
dump_path = config.get("User", "dump_path")
db_user = config.get("Database", 'db_user')
db_password = config.get("Database", "db_password")
db_address = config.get("Database", "db_address")
db_port = config.get("Database", "db_port")
db_name = config.get("Database", "db_name")

app = Flask(__name__)
# define database engine, format: engine://user:password@host:port/database
app.config['SQLALCHEMY_DATABASE_URI'] = (
    f'postgresql://{db_user}:{db_password}@{db_address}:{db_port}/{db_name}')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'topsecretkey'
dirlist = ['RedHat', 'Debian', 'Arch', 'SUSE', 'Gentoo', 'BSD']

db.init_app(app)
migrate = Migrate(app, db)

# ------------------------------- Main Routes ------------------------------- #
# open new form input page after pressing "Add Form"
@app.route('/form', methods=['POST', 'GET'])
def form():
    # hosts_query = db.session.query(CreateForm.hostname)

    # unit_query = (db.session.query(CreateUnits.unit_name)
    #                         .order_by(CreateUnits.unit_name))
    
    # level_query = (db.session.query(CreateUnits.unit_functions, 
    #                                 CreateUnits.unit_subsystems)
    #                          .order_by(CreateUnits.unit_name))

    hosts = [instance[0] for instance in Tools(db).host_query()]
    orgunits = [unit[0] for unit in Tools(db).unit_query()]
    level_data = [list(instance) for instance in Tools(db).data_query()]
    level_dict = [[c, [cd[0], cd[1]]] for c, cd in zip(orgunits, level_data)]

    if request.method == 'POST':
        new_form = CreateForm(
                name=request.form['name'],
                hostname=request.form['hostname'],
                unit_belong=request.form['unit_belong'],
                ip=request.form['ip'],
                distro=request.form['distro'],
                functions=request.form['functions'],
                subsystems=request.form['subsystems'])

        if new_form.hostname in hosts:
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
                               units=orgunits,
                               hosts=json.dumps(hosts),
                               unit_data=json.dumps(level_dict))

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

    hosts_query = db.session.query(CreateForm.hostname)

    unit_query = (db.session.query(CreateUnits.unit_name)
                            .order_by(CreateUnits.unit_name))
    
    level_query = (db.session.query(CreateUnits.unit_functions, 
                                    CreateUnits.unit_subsystems)
                             .order_by(CreateUnits.unit_name))

    hosts = [instance[0] for instance in hosts_query]
    orgunits = [unit[0] for unit in unit_query]
    level_data = [list(instance) for instance in level_query]
    level_dict = [[c, [cd[0], cd[1]]] for c, cd in zip(orgunits, level_data)]

    if request.method == 'POST':
        eips = request.form.getlist('extra_ips[]')
        ip_index = 0

        form.name=request.form['name']
        form.hostname=request.form['hostname']
        form.unit_belong=request.form['unit_belong'],
        form.ip=request.form['ip']
        for instance in db.session.query(CreateExIP).order_by(CreateExIP.id):
            if instance.forms_id == id:
                instance.extra_ip = eips[ip_index]
                ip_index += 1
        form.distro=request.form['distro']
        form.functions=request.form['functions']
        form.subsystems=request.form['subsystems']

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
                               hosts=json.dumps(hosts), units=orgunits, 
                               unit_data=json.dumps(level_dict))

# Save all database data into csv file
@app.route('/dump', methods=['GET'])
def dump():
    exip_dict = dict
    extra_ip_query = db.session.query(CreateExIP).order_by(CreateExIP.id)

    for instance in extra_ip_query:
        if str(instance.forms_id) in exip_dict:
            exip_dict[str(instance.forms_id)] += '\r\n' + instance.extra_ip
        else:
            exip_dict[str(instance.forms_id)] = instance.extra_ip

    now = datetime.now().replace(microsecond=0)
    timestamp = f"{now.date()}_{now.time()}".replace(':','-')
    dump_file = f'{dump_path}/dump_{timestamp}.csv'
    header = ['Name', 'Hostname', 'IP', 
              'Extra IPs', 'Functions', 'Subsystems']

    with open(dump_file, 'w', encoding='UTF8') as dump:
        writer = csv.writer(dump)
        writer.writerow(header)
        form_query = db.session.query(CreateForm).order_by(CreateForm.id)
        for instance in form_query:
            try:
                exip_csv = exip_dict[str(instance.id)]
            except:
                exip_csv = ''
            row_data = [instance.name, instance.hostname, instance.ip, 
                        exip_csv, instance.functions, instance.subsystems]
            writer.writerow(row_data)

    return send_file(dump_file, mimetype='text/csv', 
                     download_name='db_dump.csv')

# main page
@app.route('/', methods=['GET', 'POST'])
def index():
    forms = CreateForm.query.order_by(CreateForm.date_created).all()
    return render_template('index.html', forms=forms)


# ---------------------------- Org. Unit Routes ----------------------------- #
@app.route('/unit_new', methods=['POST', 'GET'])
def unit_new():
    clusters_query = db.session.query(CreateUnits.cluster)
    container_query = db.session.query(CreateUnits.containerization)
    pod_query = db.session.query(CreateUnits.pod)

    clusters = set([instance[0] for instance in clusters_query])
    containerizations = set([instance[0] for instance in container_query])
    pods = set([instance[0] for instance in pod_query])

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
    hosts = [instance for instance in db.session.query(CreateForm)]

    if request.method == 'POST':
        for h in hosts:
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
    hosts = [instance for instance in db.session.query(CreateForm)]

    try:
        for h in hosts:
            if h.unit_belong == unit_to_delete.unit_name:
                h.unit_belong = None

        db.session.delete(unit_to_delete)
        db.session.commit()
        return redirect('/unit')
    except:
        return "Failed to Delete Form"

@app.route('/unit', methods=['POST', 'GET'])
def unit():
    hosts_query = db.session.query(CreateForm.hostname, 
                                   CreateForm.unit_belong)

    units = (CreateUnits.query
                        .order_by(CreateUnits.date_created).all())

    hosts = [instance for instance in hosts_query]
    hc = {cl.unit_name: list() for cl in units}
    [hc[h[1]].append(h[0]) for h in hosts if h[1] in hc.keys()]

    return render_template('unit.html', units=units, hc_dict=hc)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

