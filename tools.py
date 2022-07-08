from datetime import datetime
from models import CreateForm, CreateExIP, CreateUnits

class DB_Tools():
    def __init__(self, db):
        self.db = db

    def get_form(self):
        return self.db.session.query(CreateForm)

    def get_unit(self):
        return self.db.session.query(CreateUnits)

    def get_extra_ip(self):
        return self.db.session.query(CreateExIP)        

    def host_query(self):
        return (self.db.session.query(CreateForm.hostname)
                               .order_by(CreateForm.hostname))

    def host_unit_query(self):
        return (self.db.session.query(CreateForm.hostname, 
                                      CreateForm.unit_belong))

    def extra_ip_query(self):
        return (self.db.session.query(CreateExIP)
                       .order_by(CreateExIP.id))

    def unit_query(self):
        return (self.db.session.query(CreateUnits.unit_name)
                               .order_by(CreateUnits.unit_name))

    def data_query(self):
        return (self.db.session.query(CreateUnits.unit_functions,
                                 CreateUnits.unit_subsystems)
                               .order_by(CreateUnits.unit_name))

    def model_units_query(self):
        return (CreateUnits.query
                           .order_by(CreateUnits.date_created).all())

class Tools():
    def __init__(self):
        pass

    def timestamp(self):
        now = datetime.now().replace(microsecond=0)
        return f"{now.date()}_{now.time()}".replace(':','-')

