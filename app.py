from flask import Flask, redirect, render_template
from flask import request, redirect
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import INET
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://labbrat:password@localhost:5433/masq_forms'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class CreateForm(db.Model):
    __tablename__ = 'forms'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    hostname = db.Column(db.String(30), nullable=False)
    ip = db.Column(INET)
    extra_ips = db.relationship('CreateExIP', cascade="all,delete", backref='forms')
    functions = db.Column(db.String(30), nullable=False)
    subsystems = db.Column(db.String(30), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, name, hostname, ip, functions, subsystems):
        self.name = name
        self.hostname = hostname
        self.ip = ip
        self.functions = functions
        self.subsystems = subsystems

    def __repr__(self) -> str:
        return '<Form %r>' % self.id

class CreateExIP(db.Model):
    __tablename__ = 'extra_ips'

    id = db.Column(db.Integer, primary_key=True)
    forms_id = db.Column(db.Integer, ForeignKey("forms.id"))
    extra_ip = db.Column(INET)

    def __init__(self, forms_id, extra_ip) :
        self.forms_id = forms_id
        self.extra_ip = extra_ip
    
    def __repr__(self) -> str:
        return '<ExIP %r>' % self.id

@app.route('/form', methods=['POST', 'GET'])
def form():
    if request.method == 'POST':
        new_form = CreateForm(
                name=request.form['name'],
                hostname=request.form['hostname'],
                ip=request.form['ip'],
                functions=request.form['functions'],
                subsystems=request.form['subsystems'])

        db.session.add(new_form)
        db.session.flush()

        extra_ip = request.form.getlist('field[]')
        new_extra_ips = [CreateExIP(forms_id=new_form.id, extra_ip=ip) for ip in extra_ip]
        db.session.add_all(new_extra_ips)

        db.session.commit()
        return redirect('/')

    else:
        return render_template('form.html')

@app.route('/delete/<int:id>')
def delete(id):
    form_to_delete = CreateForm.query.get_or_404(id)

    try:
        db.session.delete(form_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return "Failed to Delete Form"

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    form = CreateForm.query.get_or_404(id)

    if request.method == 'POST':
        form.name=request.form['name']
        form.hostname=request.form['hostname']
        form.ip=request.form['ip']
        form.extra_ips = request.form['extra_ips']
        form.functions=request.form['functions']
        form.subsystems=request.form['subsystems']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return "Failed to Update Form"
    else:
        return render_template('update.html', form=form)

@app.route('/', methods=['GET', 'POST'])
def index():
    forms = CreateForm.query.order_by(CreateForm.date_created).all()
    return render_template('index.html', forms=forms)
        

if __name__ == '__main__':
    app.run(debug=True)
