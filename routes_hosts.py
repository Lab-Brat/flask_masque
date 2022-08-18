from flask import Blueprint
from flask import request, render_template, redirect, send_file
from werkzeug.utils import secure_filename
from models import db, CreateForm, CreateExIP
from tools import Tools, DB_Tools
import os
import json


T = Tools()
DBT = DB_Tools(db)
routes_hosts = Blueprint("routes_hosts", __name__)

# open form to register host information
@routes_hosts.route('/form', methods = ['POST', 'GET'])
def form():
    if request.method == 'POST':
        new_form = CreateForm(
                name = request.form['name'],
                hostname = request.form['hostname'],
                unit_belong = request.form['unit_belong'],
                ip = request.form['ip'],
                distro = request.form['distro'],
                functions = request.form['functions'],
                subsystems = request.form['subsystems'])

        if T.check_host_existence(new_form) is False:
            return ('HOSTNAME EXISTS!!!'
                    'Next time please click on "Check Hostname"'
                    'button before filling out the whole form!')

        db.session.add(new_form)
        db.session.flush()

        extra_ip = request.form.getlist('field[]')
        new_extra_ips = [CreateExIP(forms_id = new_form.id, 
                                    extra_ip = ip) for ip in extra_ip]
        db.session.add_all(new_extra_ips)
        db.session.commit()
        return redirect('/')

    else:
        return render_template('form.html',
                        dirlist = T.dirlist, 
                        units = DBT.unit_query(),
                        hosts = json.dumps(DBT.host_query()),
                        unit_data = json.dumps(DBT.data_query()))

#delete form after pressing "Delete" link
@routes_hosts.route('/delete/<int:id>')
def delete(id):
    form_to_delete = CreateForm.query.get_or_404(id)
    db.session.delete(form_to_delete)
    db.session.commit()
    return redirect('/')

# open update page after pressing "Update" link
@routes_hosts.route('/update/<int:id>', methods = ['GET', 'POST'])
def update(id):
    form = CreateForm.query.get_or_404(id)

    if request.method == 'POST':
        form.name = request.form['name']
        form.hostname = request.form['hostname']
        form.unit_belong = request.form['unit_belong'],
        form.ip = request.form['ip']
        form.distro = request.form['distro']
        form.functions = request.form['functions']
        form.subsystems = request.form['subsystems']

        # change existring extra IPs
        exip_form = request.form.getlist('extra_ips[]')
        exip_db = [ip for ip in DBT.extra_ip_query()
                             if ip.forms_id == id]
        for i, ip in enumerate(exip_form):
            exip_db[i].extra_ip = ip

        # process newly created extra IPs
        extra_ip = request.form.getlist('field[]')
        new_extra_ips = [CreateExIP(forms_id = form.id, 
                                    extra_ip = ip) for ip in extra_ip]

        db.session.add_all(new_extra_ips)
        db.session.commit()
        return redirect('/')

    else:
        return render_template('update.html', form = form, 
                        dirlist = T.dirlist,
                        units = DBT.unit_query(),
                        hosts = json.dumps(DBT.host_query()),
                        unit_data = json.dumps(DBT.data_query()))

# Save all database data into csv file
@routes_hosts.route('/dump', methods = ['GET'])
def dump():
    dump_file = f'./dumps/dump_{T.timestamp()}.csv'
    os.makedirs(os.path.dirname(dump_file), exist_ok = True)

    T.write_csv(dump_file)

    return send_file(dump_file, mimetype = 'text/csv', 
                     download_name = 'db_dump.csv')

# Upload hosts infromation to the app
@routes_hosts.route('/upload_csv', methods = ['GET', 'POST'])
def upload_csv():
    if request.method == 'POST':
        file = request.files['file']
        filename = secure_filename(file.filename).split('.')

        if T._extension_check(filename):
            filename = filename[0] + f"_{T.timestamp()}" + ".csv"
            os.makedirs(os.path.dirname('uploads/'), exist_ok = True)
            file.save(os.path.join('uploads/', filename))

            header, content = T._read_csv(filename)
            new_forms = T.extract_csv_form(header, content)

            for form in new_forms:
                if T.check_host_existence(form):
                    try:
                        db.session.add(form)
                    except:
                        return new_forms 
                else:
                    return f'HOSTNAME {form.hostname} EXISTS in DB!!!'
            db.session.flush()
            
            db.session.add_all(T.extract_csv_exip(content, new_forms))
            db.session.commit()

            return redirect('/')
        else:
            return 'Wrong File Extension'
    return render_template('upload_csv.html')

# main page
@routes_hosts.route('/', methods = ['GET', 'POST'])
def index():
    forms = DBT.get_model('form')
    return render_template('index.html', forms = forms)
