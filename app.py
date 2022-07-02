from flask import Flask
from flask import request, redirect, render_template, send_file
from flask_migrate import Migrate
from models import db, CreateForm, CreateExIP, CreateClusters
from datetime import datetime
import configparser
import csv
import json


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
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{db_user}:{db_password}@{db_address}:{db_port}/{db_name}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'topsecretkey'
dirlist = ['RedHat', 'Debian', 'Arch', 'SUSE', 'Gentoo', 'BSD']

db.init_app(app)
migrate = Migrate(app, db)

#--------------------- main routes ---------------------#
# open new form input page after pressing "Add Form"
@app.route('/form', methods=['POST', 'GET'])
def form():
    hosts = [instance[0] for instance in db.session.query(CreateForm.hostname)]
    clusters = [instance[0] for instance in db.session.query(CreateClusters.cluster)]
    cluster_data = [list(instance) for instance in db.session.query(
                        CreateClusters.cluster_functions, 
                        CreateClusters.cluster_subsystems)]
    cluster_dict = [[c, [cd[0], cd[1]]] for c, cd in zip(clusters, cluster_data)]

    if request.method == 'POST':
        new_form = CreateForm(
                name=request.form['name'],
                hostname=request.form['hostname'],
                cluster_belong=request.form['cluster_belong'],
                ip=request.form['ip'],
                distro=request.form['distro'],
                functions=request.form['functions'],
                subsystems=request.form['subsystems'])

        if new_form.hostname in hosts:
            return 'HOSTNAME EXISTS!!!\
                    Next time please click on "Check Hostname" button before filling out the whole form!'

        db.session.add(new_form)
        db.session.flush()

        extra_ip = request.form.getlist('field[]')
        new_extra_ips = [CreateExIP(forms_id=new_form.id, extra_ip=ip) for ip in extra_ip]
        db.session.add_all(new_extra_ips)

        db.session.commit()
        return redirect('/')

    else:
        return render_template('form.html', hosts=json.dumps(hosts), dirlist=dirlist,
                                    clusters=clusters, cluster_data=json.dumps(cluster_dict))

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
    hosts = [instance[0] for instance in db.session.query(CreateForm.hostname)]
    clusters = [instance[0] for instance in db.session.query(CreateClusters.cluster)]
    cluster_data = [list(instance) for instance in db.session.query(
                        CreateClusters.cluster_functions, 
                        CreateClusters.cluster_subsystems)]
    cluster_dict = [[c, [cd[0], cd[1]]] for c, cd in zip(clusters, cluster_data)]

    if request.method == 'POST':
        eips = request.form.getlist('extra_ips[]')
        ip_index = 0

        form.name=request.form['name']
        form.hostname=request.form['hostname']
        form.cluster_belong=request.form['cluster_belong'],
        form.ip=request.form['ip']
        for instance in db.session.query(CreateExIP).order_by(CreateExIP.id):
            if instance.forms_id == id:
                instance.extra_ip = eips[ip_index]
                ip_index += 1
        form.distro=request.form['distro']
        form.functions=request.form['functions']
        form.subsystems=request.form['subsystems']

        extra_ip = request.form.getlist('field[]')
        new_extra_ips = [CreateExIP(forms_id=form.id, extra_ip=ip) for ip in extra_ip]
        db.session.add_all(new_extra_ips)

        try:
            db.session.commit()
            return redirect('/')
        except:
            return "Failed to Update Form"
    else:
        return render_template('update.html', form=form, hosts=json.dumps(hosts), dirlist=dirlist, 
                                clusters=clusters, cluster_data=json.dumps(cluster_dict))

# Save all database data into csv file
@app.route('/dump', methods=['GET'])
def dump():
    exip_dict = {}
    for instance in db.session.query(CreateExIP).order_by(CreateExIP.id):
        if str(instance.forms_id) in exip_dict:
            exip_dict[str(instance.forms_id)] += '\r\n' + instance.extra_ip
        else:
            exip_dict[str(instance.forms_id)] = instance.extra_ip

    timestamp = f"{str(datetime.now())[0:10]}_{str(datetime.now())[12:19]}"
    dump_file = f'{dump_path}/dump_{timestamp}.csv'
    header = ['Name', 'Hostname', 'IP', 'Extra IPs', 'Functions', 'Subsystems']

    with open(dump_file, 'w', encoding='UTF8') as dump:
        writer = csv.writer(dump)
        writer.writerow(header)
        for instance in db.session.query(CreateForm).order_by(CreateForm.id):
            try:
                exip_csv = exip_dict[str(instance.id)]
            except:
                exip_csv = ''
            row_data = [ instance.name, instance.hostname, instance.ip, exip_csv, 
                         instance.functions, instance.subsystems]
            writer.writerow(row_data)

    return send_file(dump_file, mimetype='text/csv', download_name='db_dump.csv')

# main page
@app.route('/', methods=['GET', 'POST'])
def index():
    forms = CreateForm.query.order_by(CreateForm.date_created).all()
    return render_template('index.html', forms=forms)


#--------------------- cluster routes ---------------------#
@app.route('/cluster_new', methods=['POST', 'GET'])
def cluster_new():
    if request.method == 'POST':
        new_cluster = CreateClusters(unit_name=request.form['unit_name'],
                            unit_level=request.form['unit_level'],
                            description=request.form['description'],
                            cluster=request.form['cluster'],
                            containerization=request.form['containerization'],
                            pods=request.form['pods'],
                            cluster_functions=request.form['cluster_functions'],
                            cluster_subsystems=request.form['cluster_subsystems'])

        db.session.add(new_cluster)
        db.session.commit()

        return redirect('/cluster')
    else:
        return render_template('cluster_new.html') 

@app.route('/cluster_update/<int:id>', methods=['POST', 'GET'])
def cluster_update(id):
    cluster = CreateClusters.query.get_or_404(id)
    hosts = [instance for instance in db.session.query(CreateForm)]

    if request.method == 'POST':
        for h in hosts:
            if h.cluster_belong == cluster.cluster:
                h.cluster_belong = request.form['cluster']

        cluster.cluster = request.form['cluster']
        cluster.description = request.form['description']
        cluster.cluster_functions = request.form['cluster_functions']
        cluster.cluster_subsystems = request.form['cluster_subsystems']

        db.session.commit()

        return redirect('/cluster')
    else:
        return render_template('cluster_update.html', cluster=cluster)  


@app.route('/cluster_delete/<int:id>', methods=['POST', 'GET'])
def cluster_delete(id):
    form_to_delete = CreateClusters.query.get_or_404(id)

    try:
        db.session.delete(form_to_delete)
        db.session.commit()
        return redirect('/cluster')
    except:
        return "Failed to Delete Form"

@app.route('/cluster', methods=['POST', 'GET'])
def cluster():
    clusters = CreateClusters.query.order_by(CreateClusters.date_created).all()
    hosts = [instance for instance in db.session.query(CreateForm.hostname, CreateForm.cluster_belong)]
    
    hc = {cl.cluster: list() for cl in clusters}
    [hc[h[1]].append(h[0]) for h in hosts if h[1] in hc.keys()]

    return render_template('cluster.html', clusters=clusters, hc_dict=hc)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

