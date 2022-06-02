## flask_masque

#### Introduction
Small web-forms app, allows a user to record some information about his VMs, like hostname, IP address, describtion etc.  
Main logic is built with Python's Flask framework and HTML, with a small addition of CSS and JS.  
Data is stored in PostgreSQL database.  
Repository comes with an Ansible playbook (at ../linux_scripts/ansible) to configure the app and the database on Alma Linux 8.  

#### Install
Follow the steps to install and use the app:
* download the repository and navigate to it
```
git clone https://github.com/Lab-Brat/flask_masque.git
cd flask_masque
```
* Install the dependencies:  
```
python -m pip install --upgrade pip
python -m pip install Flask psycopg2 flask-migrate sqlalchemy
```
* install PostgrSQL on Alma Linux 8:
```
sudo dnf install postgresql-server postgresql
```
* enable service and initialize database
```
postgresql-setup initdb
sudo systemctl enable --now postgresql
```
* configure support for remote access:
```
sudo vim /var/lib/pgsql/data/postgresql.conf  #--->listen_addresses = '*'
                                              #--->port = 5433
sudo vim /var/lib/pgsql/data/pg_hba.conf  #------->host all all 0.0.0.0/0 md5
sudo systemctl restart postgresql
```
* configure PostgreSQL
```
# change master password
sudo su - postgres
psql -c "alter user postgres with password 'StrongPassword'"

# login to cli and create new role and the database
psql
CREATE ROLE <user> SUPERUSER CREATEDB LOGIN PASSWORD 'password';
CREATE DATABASE infra_forms;
GRANT ALL PRIVILEGES ON DATABASE infra_forms TO <user>;

# exit
\q
exit
```
* set the environment and poulate database
```
export FLASK_APP=app.py
export FLASK_ENV=development
flask db init && flask db migrate && flask db upgrade
```
* run the app!
```
flask run
# open browser, enter http://127.0.0.1:5000
```
