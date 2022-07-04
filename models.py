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
    cluster_belong = db.Column(db.String(30))
    ip = db.Column(INET)
    extra_ips = db.relationship('CreateExIP', 
                                cascade="all,delete", backref='forms')
    distro = db.Column(db.String(20), nullable=False)
    functions = db.Column(db.String(200), nullable=False)
    subsystems = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, 
                             default=datetime.now().replace(microsecond=0))

    def __init__(self, name, hostname, cluster_belong, 
                 ip, distro, functions, subsystems):
        self.name = name
        self.hostname = hostname
        self.ip = ip
        self.cluster_belong = cluster_belong
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


class CreateClusters(db.Model):
    '''
    Database model for organizational units
    '''
    __tablename__ = 'cluster_forms'

    id = db.Column(db.Integer, primary_key=True)
    unit_name = db.Column(db.String(50), nullable=False)
    unit_level = db.Column(db.String(20), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    cluster = db.Column(db.String(50), nullable=False)
    containerization = db.Column(db.String(50))
    pods = db.Column(db.String(50))
    cluster_functions = db.Column(db.String(200))
    cluster_subsystems = db.Column(db.String(200))
    date_created = db.Column(db.DateTime, 
                             default=datetime.now().replace(microsecond=0))

    def __init__(self, unit_name, unit_level, description, 
                 cluster, containerization, pods, 
                 cluster_functions, cluster_subsystems):
        self.unit_name = unit_name
        self.unit_level = unit_level
        self.description = description
        self.cluster = cluster
        self.containerization = containerization
        self.pods = pods
        self.cluster_functions = cluster_functions 
        self.cluster_subsystems = cluster_subsystems

    def __repr__(self) -> str:
        return '<Cluster %r>' % self.id
