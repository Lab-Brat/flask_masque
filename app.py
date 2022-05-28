from flask import Flask, redirect, render_template, url_for
from flask import request, redirect
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import INET
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/infra_forms'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class CreateForm(db.Model):
    __tablename__ = 'forms_table'

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200), nullable=False)
    name = db.Column(db.String(30), nullable=False)
    hostname = db.Column(db.String(30), nullable=False)
    ip = db.Column(INET)
    functions = db.Column(db.String(30), nullable=False)
    subsystems = db.Column(db.String(30), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, description, name, hostname, ip,
                       functions, subsystems):
        self.description = description
        self.name = name
        self.hostname = hostname
        self.ip = ip
        self.functions = functions
        self.subsystems = subsystems

    def __repr__(self) -> str:
        return '<Form %r>' % self.id

@app.route('/form', methods=['POST', 'GET'])
def form():
    if request.method == 'POST':
        if request.form['submit_button'] == 'Finish':
            new_form = CreateForm(description=request.form['description'],
                            name=request.form['name'],
                            hostname=request.form['hostname'],
                            ip=request.form['ip'],
                            functions=request.form['functions'],
                            subsystems=request.form['subsystems'])

            db.session.add(new_form)
            db.session.commit()
            return redirect('/')
        elif request.form['submit_button'] == 'Add':
            return url_for('static', filename='js/add_ip.js')

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
        form.description=request.form['description']
        form.name=request.form['name']
        form.hostname=request.form['hostname']
        form.ip=request.form['ip']
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
    if request.method == 'POST':
        fullname = request.form.getlist('field[]')
        for value in fullname:
            print(f"###########  {value}  ############")
            # cur.execute("INSERT INTO fullnames (full_name) VALUES (%s)",[value])
            # mysql.connection.commit()
            # cur.close()
        message = "Succesfully Register"
    else:
        forms = CreateForm.query.order_by(CreateForm.date_created).all()
        return render_template('index.html', forms=forms)
        

if __name__ == '__main__':
    app.run(debug=True)
