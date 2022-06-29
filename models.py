from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import INET
from datetime import datetime


db = SQLAlchemy()

class CreateForm(db.Model):
    '''
    Database model for the form (except extra IPs)
    '''
    __tablename__ = 'forms'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    hostname = db.Column(db.String(30), nullable=False)
    cluster_belong = db.Column(db.String(30))
    ip = db.Column(INET)
    extra_ips = db.relationship('CreateExIP', cascade="all,delete", backref='forms')
    distro = db.Column(db.String(20), nullable=False)
    functions = db.Column(db.String(200), nullable=False)
    subsystems = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.now().replace(microsecond=0))

    def __init__(self, name, hostname, cluster_belong, ip, distro, functions, subsystems):
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

class CreateClusters(db.Model):
    __tablename__ = 'cluster_forms'

    id = db.Column(db.Integer, primary_key=True)
    cluster = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    cluster_functions = db.Column(db.String(200))
    cluster_subsystems = db.Column(db.String(200))
    date_created = db.Column(db.DateTime, default=datetime.now().replace(microsecond=0))

    def __init__(self, cluster, description, cluster_functions, cluster_subsystems):
        self.cluster = cluster
        self.description = description
        self.cluster_functions = cluster_functions 
        self.cluster_subsystems = cluster_subsystems

    def __repr__(self) -> str:
        return '<Cluster %r>' % self.id
