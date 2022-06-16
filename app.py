from flask import Flask
from flask import request, redirect, render_template, send_file
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import INET
from datetime import datetime
import csv, json


app = Flask(__name__)
# define database engine, format: engine://user:password@host:port/database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://labbrat:password@localhost:5433/masq_forms'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'topsecretkey'
dirlist = ['RedHat', 'Debian', 'Arch', 'SUSE', 'Gentoo', 'BSD']
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class CreateForm(db.Model):
    '''
    Database model for the form (except extra IPs)
    '''
    __tablename__ = 'forms'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    hostname = db.Column(db.String(30), nullable=False)
    ip = db.Column(INET)
    extra_ips = db.relationship('CreateExIP', cascade="all,delete", backref='forms')
    distro = db.Column(db.String(20), nullable=False)
    functions = db.Column(db.String(200), nullable=False)
    subsystems = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, name, hostname, ip, distro, functions, subsystems):
        self.name = name
        self.hostname = hostname
        self.ip = ip
        self.distro = distro
        self.functions = functions
        self.subsystems = subsystems

    def __repr__(self) -> str:
        return '<Form %r>' % self.id

class CreateExIP(db.Model):
    '''
    Database model extra IPs
    '''
    __tablename__ = 'extra_ips'

    id = db.Column(db.Integer, primary_key=True)
    forms_id = db.Column(db.Integer, ForeignKey("forms.id"))
    extra_ip = db.Column(INET)

    def __init__(self, forms_id, extra_ip) :
        self.forms_id = forms_id
        self.extra_ip = extra_ip
    
    def __repr__(self) -> str:
        return '<ExIP %r>' % self.id

# open new form input page after pressing "Add Form"
@app.route('/form', methods=['POST', 'GET'])
def form():
    hosts = [instance[0] for instance in db.session.query(CreateForm.hostname)]
    if request.method == 'POST':
        new_form = CreateForm(
                name=request.form['name'],
                hostname=request.form['hostname'],
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
        return render_template('form.html', hosts=json.dumps(hosts), dirlist=dirlist)

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
        eips = request.form.getlist('extra_ips[]')
        ip_index = 0

        form.name=request.form['name']
        form.hostname=request.form['hostname']
        form.ip=request.form['ip']
        for instance in db.session.query(CreateExIP).order_by(CreateExIP.id):
            if instance.forms_id == id:
                instance.extra_ip = eips[ip_index]
                ip_index += 1
        form.distro=request.form['distro']
        form.functions=request.form['functions']
        form.subsystems=request.form['subsystems']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return "Failed to Update Form"
    else:
        return render_template('update.html', form=form, dirlist=dirlist)

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
    dump_path = f'/home/labbrat/dumps/dump_{timestamp}.csv'
    header = ['Name', 'Hostname', 'IP', 'Extra IPs', 'Functions', 'Subsystems']

    with open(dump_path, 'w', encoding='UTF8') as dump:
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

    return send_file(dump_path, mimetype='text/csv', download_name='db_dump.csv')

# main page
@app.route('/', methods=['GET', 'POST'])
def index():
    forms = CreateForm.query.order_by(CreateForm.date_created).all()
    return render_template('index.html', forms=forms)


if __name__ == '__main__':
    app.run(debug=True)

