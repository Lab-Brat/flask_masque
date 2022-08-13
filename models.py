from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import INET
from datetime import datetime
from dataclasses import dataclass


db = SQLAlchemy()

@dataclass
class CreateForm(db.Model):
    '''
    Database model for the main forms
    '''
    __tablename__ = 'forms'
    id: str = db.Column(db.Integer, primary_key=True)
    name: str = db.Column(db.String(30), nullable=False)
    hostname: str = db.Column(db.String(30), nullable=False)
    unit_belong: str = db.Column(db.String(30))
    ip: str = db.Column(INET)
    extra_ips: str = db.relationship('CreateExIP', 
                                cascade="all,delete", backref='forms')
    distro: str = db.Column(db.String(20), nullable=False)
    functions: str = db.Column(db.String(200), nullable=False)
    subsystems: str = db.Column(db.String(200), nullable=False)
    date_created: str = db.Column(db.DateTime, 
                            default=datetime.now().replace(microsecond=0))

    def __repr__(self) -> str:
        return '<Form %r>' % self.id


@dataclass
class CreateExIP(db.Model):
    '''
    Database model for extra IP addresses
    '''
    __tablename__ = 'extra_ips'

    id: str = db.Column(db.Integer, primary_key=True)
    forms_id: str = db.Column(db.Integer, ForeignKey("forms.id"))
    extra_ip: str = db.Column(INET)
    
    def __repr__(self) -> str:
        return '<ExIP %r>' % self.id


class CreateUnits(db.Model):
    '''
    Database model for organizational units
    '''
    __tablename__ = 'units_forms'

    id: str = db.Column(db.Integer, primary_key=True)
    unit_name: str = db.Column(db.String(50), nullable=False)
    unit_level: str = db.Column(db.String(20), nullable=False)
    description: str = db.Column(db.String(200), nullable=False)
    cluster: str = db.Column(db.String(50), nullable=False)
    containerization: str = db.Column(db.String(50))
    pod: str = db.Column(db.String(50))
    unit_functions: str = db.Column(db.String(200))
    unit_subsystems: str = db.Column(db.String(200))
    date_created: str = db.Column(db.DateTime, 
                             default=datetime.now().replace(microsecond=0))

    def __repr__(self) -> str:
        return '<Unit %r>' % self.id
