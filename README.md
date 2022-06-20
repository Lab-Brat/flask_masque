# flask_masque

## Table of Contents
- [Introduction](#introduction)
- [Configuration](#configuration)
- [Installation](#installation)
  - [Docker](#docker)
  - [Ansible](#ansible)
  - [Manual](#manual)

## Introduction
Small web-forms app, allows a user to record some information about his VMs, like hostname, IP address, describtion etc.  
Main logic is built with Python's Flask framework and HTML, with a small addition of CSS and JS.  
Data is stored in PostgreSQL database.  
Repository comes with an Ansible playbook (at ../linux_scripts/ansible) to configure the app and the database on Alma Linux 8.  

## Configuration 
There is a configuration file in the repository that needs to be filled out for the app to work properly. Required fields:  
* dump_path -> path where the database dumps will be saved on the system
* sample_entries -> sample entries that will be added to the database after the installation
* db_user -> admin user for the created tables in PostgreSQL
* db_password -> password for the admin user
* db_address -> IP address or hostname of the database (usually localhost)
* db_port -> port which PostgreSQL will be listening on
* db_name -> name of the database where everything will be stored

## Installation
#### Docker
* make sure that Docker is installed on your system. To install on AlmaLinux:
```console
sudo yum install -y yum-utils
sudo yum-config-manager --add-repo \
     https://download.docker.com/linux/centos/docker-ce.repo
sudo yum install docker-ce docker-ce-cli containerd.io docker-compose-plugin
sudo systemctl start docker
sudo usermod -aG docker <user>
```
* download the repository and navigate to it
```console
git clone https://github.com/Lab-Brat/flask_masque.git
cd flask_masque
```
* run docker-compose, it will build the image containing the app and create two containers - postgresql and the app  
**\# Note that in this case the repository will be mounted into the container**
```console
docker-compose -f Docker/docker-compose.yml up
```

#### Ansible
* download Ansible playbook from my GitHub
```
wget https://raw.githubusercontent.com/Lab-Brat/linux_scripts/main/ansible/app_forms.yaml
```
* add your host to the inventory file, and run the playbook 
```
ansible-playbook app_forms.yaml --limit <host>
```

#### Manual
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
* create a directory for database dumps
```
mkdir ~/dumps
```
* run the app!
```
flask run
# open browser, enter http://127.0.0.1:5000
```
