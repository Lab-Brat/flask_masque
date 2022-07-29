from flask import Blueprint
from flask import request, render_template, redirect, send_file
from werkzeug.utils import secure_filename
from models import db, CreateForm, CreateExIP
from tools import Tools, DB_Tools
import os
import csv
import json


dirlist = Tools().dirlist
routes_hosts = Blueprint("routes_hosts", __name__)

# open form to register host information
@routes_hosts.route('/form', methods=['POST', 'GET'])
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

#delete form after pressing "Delete" link
@routes_hosts.route('/delete/<int:id>')
def delete(id):
    form_to_delete = CreateForm.query.get_or_404(id)

    try:
        db.session.delete(form_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return "Failed to Delete Form"

# open update page after pressing "Update" link
@routes_hosts.route('/update/<int:id>', methods=['GET', 'POST'])
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
@routes_hosts.route('/dump', methods=['GET'])
def dump():
    exip_dict = Tools().prepare_csv(db)
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

@routes_hosts.route('/upload_csv', methods=['GET', 'POST'])
def upload_csv():
    if request.method == 'POST':
        file = request.files['file']
        filename = secure_filename(file.filename)
        os.makedirs(os.path.dirname('uploads/'), exist_ok=True)
        file.save(os.path.join('uploads/', filename))

        with open(f"uploads/{filename}", 'r') as f:
            csvreader = csv.reader(f)
            header = next(csvreader)
            content = [row for row in csvreader]

        for data in content:
            if len(data) != len(header):
                return f"Wrong Column Count in host: {data[0]}"
            else:
                new_form = CreateForm(name = data[0],hostname = data[1],
                                unit_belong = data[2],
                                ip=data[3], distro=data[4],
                                functions = data[5], subsystems = data[6])

                db.session.add(new_form)
                db.session.flush()

                exip = data[4].split('\n')
                if exip != ['']:
                    ne = [CreateExIP(forms_id = new_form.id, 
                                     extra_ip = ip) for ip in exip]
                    db.session.add_all(ne)

                db.session.commit()
            

        return redirect('/')
    return render_template('upload_csv.html')

# main page
@routes_hosts.route('/', methods=['GET', 'POST'])
def index():
    forms = DB_Tools(db).get_model('form')
    return render_template('index.html', forms=forms)
