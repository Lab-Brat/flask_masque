from models import CreateForm, CreateExIP, CreateUnits

class Tools():
    def __init__(self, db):
        self.db = db

    def host_query(self):
        return (self.db.session.query(CreateForm.hostname)
                               .order_by(CreateForm.hostname))
    def unit_query(self):
        return (self.db.session.query(CreateUnits.unit_name)
                               .order_by(CreateUnits.unit_name))

    def data_query(self):
        return (self.db.session.query(CreateUnits.unit_functions,
                                 CreateUnits.unit_subsystems)
                               .order_by(CreateUnits.unit_name))
