import csv
from datetime import datetime
from collections import defaultdict
from models import db
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
        self.dirlist = ['RedHat', 'Debian', 'Arch', 'SUSE', 'Gentoo', 'BSD']
        self.header =  ['Name', 'Hostname', 'Org. Unit', 'IP', 
                        'Extra IPs', 'Distro', 'Functions', 'Subsystems']

    def timestamp(self):
        now = datetime.now().replace(microsecond=0)
        return f"{now.date()}_{now.time()}".replace(':','-')

    def get_lvl_checklist(self, unit):
        unit_lvl_checks = ['false', 'false', 'false']
        for i, lvl in enumerate(unit_lvl_checks):
            if unit.unit_level == 'cluster':
                unit_lvl_checks[0] = 'checked'
            elif unit.unit_level == 'containerization':
                unit_lvl_checks[1] = 'checked'
            elif unit.unit_level == 'pod':
                unit_lvl_checks[2] = 'checked'
        return unit_lvl_checks

    def check_host_existence(self, form):
        if form.hostname in DB_Tools(db).host_query():
            return False
        else:
            return True

    def prepare_csv(self):
        exip_dict = defaultdict(list)
        for instance in DB_Tools(db).extra_ip_query():
            exip_dict[str(instance.forms_id)].append(instance.extra_ip)

        return {key: '\r\n'.join(exip_dict[key]) for key in exip_dict}

    def write_csv(self, filename):
        exip_dict = self.prepare_csv(db)
        with open(filename, 'w', encoding='UTF8') as dump:
            writer = csv.writer(dump)
            writer.writerow(self.header)
            for instance in DB_Tools(db).get_model('form'):
                try:
                    exip_csv = exip_dict[str(instance.id)]
                except:
                    exip_csv = ''
                row_data = [instance.name, instance.hostname, 
                            instance.unit_belong, 
                            instance.ip, exip_csv,
                            instance.distro,
                            instance.functions, instance.subsystems]
                writer.writerow(row_data)

    def _read_csv(self, filename):
        with open(f"uploads/{filename}", 'r') as f:
            csvreader = csv.reader(f)
            header = self.header
            next(csvreader)
            content = [row for row in csvreader]
        return header, content

    def _extension_check(self, filename):
        if filename[-1] == 'csv':
            return True
        else:
            return False

    def extract_csv_form(self, header, content):
        new_forms = []

        for data in content:
            if len(data) != len(header):
                return f"Wrong Column Count in host: {data[0]}"
            else:
                new_form = CreateForm( name = data[0],
                                hostname = data[1], unit_belong = data[2],
                                ip = data[3], distro = data[5],
                                functions = data[6], subsystems = data[7])
                new_forms.append(new_form)
        return new_forms

    def extract_csv_exip(self, content, forms):
        new_exips = []
        for data, form in zip(content, forms):
            exip = data[4].split('\n')
            if exip != ['']:
                ne = [CreateExIP(forms_id = form.id, 
                                 extra_ip = ip) for ip in exip]
                new_exips.extend(ne)
        return new_exips
