from datetime import datetime
from models import CreateForm, CreateExIP, CreateUnits

class DB_Tools():
    def __init__(self, db):
        self.db = db

    def get_model(self, model):
        if model == 'form':
            return (CreateForm.query
                               .order_by(CreateForm.date_created).all())     
        elif model == 'extra_ip':
            return (CreateExIP.query
                               .order_by(CreateExIP.id).all())
        elif model == 'unit':
            return (CreateUnits.query
                               .order_by(CreateUnits.date_created).all())

    def model_query(self, model):
        if model == 'form':
            return self.db.session.query(CreateForm).all()
        elif model == 'extra_ip':
            return self.db.session.query(CreateExIP).all()
        elif model == 'unit':
            return self.db.session.query(CreateUnits).all()

    def host_query(self):
        hosts = (self.db.session.query(CreateForm.hostname)
                                .order_by(CreateForm.hostname).all())
        return self._extract(hosts)

    def unit_query(self):
        units =  (self.db.session.query(CreateUnits.unit_name)
                                 .order_by(CreateUnits.unit_name).all())
        return self._extract(units)

    def data_query(self):
        data = (self.db.session.query(CreateUnits.unit_name,
                                      CreateUnits.unit_functions,
                                      CreateUnits.unit_subsystems)
                               .order_by(CreateUnits.unit_name).all())
        
        return [[d[0], [d[1],d[2]]] for d in data]

    def host_unit_query(self):
        return (self.db.session.query(CreateForm.hostname, 
                                      CreateForm.unit_belong).all())

    def extra_ip_query(self):
        return (self.db.session.query(CreateExIP)
                       .order_by(CreateExIP.id))

    def _extract(self, queries):
        contents = [element for query in queries for element in query]
        if len(contents) != 1 and '' in contents:
            contents.remove('')

        return list(set(contents))

    def unit_details_query(self):
        clus = self.db.session.query(CreateUnits.cluster)
        cons = self.db.session.query(CreateUnits.containerization)
        pods = self.db.session.query(CreateUnits.pod)

        return self._extract(clus), self._extract(cons), self._extract(pods)


class Tools():
    def __init__(self):
        pass

    def timestamp(self):
        now = datetime.now().replace(microsecond=0)
        return f"{now.date()}_{now.time()}".replace(':','-')
