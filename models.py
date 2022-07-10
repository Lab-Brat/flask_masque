from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import INET
from datetime import datetime


db = SQLAlchemy()

class CreateForm(db.Model):
    '''
    Database model for the main forms
    '''
    __tablename__ = 'forms'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    hostname = db.Column(db.String(30), nullable=False)
    unit_belong = db.Column(db.String(30))
    ip = db.Column(INET)
    extra_ips = db.relationship('CreateExIP', 
                                cascade="all,delete", backref='forms')
    distro = db.Column(db.String(20), nullable=False)
    functions = db.Column(db.String(200), nullable=False)
    subsystems = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, 
                             default=datetime.now().replace(microsecond=0))

    def __init__(self, name, hostname, unit_belong, 
                 ip, distro, functions, subsystems):
        self.name = name
        self.hostname = hostname
        self.unit_belong = unit_belong
        self.ip = ip
        self.distro = distro
        self.functions = functions
        self.subsystems = subsystems

    def __repr__(self) -> str:
        return '<Form %r>' % self.id


class CreateExIP(db.Model):
    '''
    Database model for extra IP addresses
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


class CreateUnits(db.Model):
    '''
    Database model for organizational units
    '''
    __tablename__ = 'units_forms'

    id = db.Column(db.Integer, primary_key=True)
    unit_name = db.Column(db.String(50), nullable=False)
    unit_level = db.Column(db.String(20), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    cluster = db.Column(db.String(50), nullable=False)
    containerization = db.Column(db.String(50))
    pod = db.Column(db.String(50))
    unit_functions = db.Column(db.String(200))
    unit_subsystems = db.Column(db.String(200))
    date_created = db.Column(db.DateTime, 
                             default=datetime.now().replace(microsecond=0))

    def __init__(self, unit_name, unit_level, description, 
                 cluster, containerization, pod, 
                 unit_functions, unit_subsystems):
        self.unit_name = unit_name
        self.unit_level = unit_level
        self.description = description
        self.cluster = cluster
        self.containerization = containerization
        self.pod = pod
        self.unit_functions = unit_functions 
        self.unit_subsystems = unit_subsystems

    def __repr__(self) -> str:
        return '<Unit %r>' % self.id
