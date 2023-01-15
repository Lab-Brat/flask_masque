# flask_masque

## Table of Contents
- [Introduction](#introduction)
- [Configuration](#configuration)
- [Installation](#installation)
  - [Docker](#docker)
  - [Ansible](#ansible)
- [Run](#run)
- [Open](#open)

## Introduction
Web application for recording and cataloging infrastructure components (VMs or containers).  
Stack: Python (Flask, psycopg2, SQLAlchemy, pytest), PostgreSQL, HTML, CSS, JS.  
There are 2 ways to deploy the app:
 * Ansible [role](https://github.com/Lab-Brat/ansible_flask) on a AlmaLinux 9 VM;
 * Docker container using Docker Compose.

## Configuration
Web app relies on environmental variables for it's configuration. They should be defined in `.env`, which will be read by Docker Compose.
* `FLASK_DEBUG` 1 or 0, set flask debug mode on or off 
* `DB_USER` admin user for the created tables in PostgreSQL
* `DB_PASS` password for the admin user
* `DB_ADDRESS` IP address or hostname of the database (usually localhost)
* `DB_PORT` port which PostgreSQL will be listening on
* `DB_NAME` name of the database where everything will be stored
* `DB_URI` database URI, uses all previous variables and doesn't need to be manually filled
* `DOMAIN_NAME` domain name that Nginx reverse proxy will route traffic to

## Installation
#### Docker
* download the repository and navigate into it
```bash
git clone https://github.com/Lab-Brat/flask_masque.git
cd flask_masque
```
* run docker-compose, it will build the app image (Debian minimal) and create three containers - nginx, postgresql and the app  
**\# Note that in this case the repository will be mounted into the container**
```bash
docker-compose up -d
```

#### Ansible
* download Ansible [role](https://github.com/Lab-Brat/ansible_flask) from my GitHub
* changed variables in `defaults/main.yaml`
* create a `site.yaml` and inventory files, import the role and run the playbook
* after playbook configures the server, navigate to the app folder and run:
```bash
flask run --host=0.0.0.0
```

#### Open
App's web interface can be opened by entering server's IP address (or hostname) and port in the search bar, for example:
```
http://192.168.0.1:5000
```
Or by using a domain name that was supplied to Nginx reverse proxy, in case where the app was deployed as a container.

#### Default User
There is a default admin user:
* username: admin@admin
* password: admin

#### Add Sample Data
Contents of directory `samples` will be mounted to `/opt` on the Docker container. 
To populate app with sample data enter container with bash shell and execute the script:
```bash
docker exec -it pg /bin/bash
sh /opt/add_entries.sh
```
