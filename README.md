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
Main logic is built with Python's Flask framework and HTML, with a small addition of CSS and JS.  
Data is stored in PostgreSQL database.  
App can be deployed either by an Ansible playbook on a virtual machine (Alma Linux 8) or in a container form using Docker.  

## Configuration 
Web app relies on environmental variables for it's configuration. They should be configured by the user in ```env.sh```, and exported to the system
```bash
source env.sh
```
* DB_USER -> admin user for the created tables in PostgreSQL
* DB_PASS -> password for the admin user
* DB_ADDRESS -> IP address or hostname of the database (usually localhost)
* DB_PORT -> port which PostgreSQL will be listening on
* DB_NAME -> name of the database where everything will be stored
* DB_URI -> database URI, uses all previous variables and doesn't need to be manually filled

## Installation
#### Docker
* make sure that Docker is installed on your system. To install on AlmaLinux:
```bash
yum install -y yum-utils
sudo yum-config-manager --add-repo \
     https://download.docker.com/linux/centos/docker-ce.repo
sudo yum install docker-ce docker-ce-cli containerd.io docker-compose-plugin
sudo systemctl start docker
sudo usermod -aG docker <user>
```
* download the repository and navigate to it
```bash
git clone https://github.com/Lab-Brat/flask_masque.git
cd flask_masque
```
* run docker-compose, it will build the image containing the app and create two containers - postgresql and the app  
**\# Note that in this case the repository will be mounted into the container**
```bash
docker-compose up
```

#### Ansible
* download Ansible playbook from my GitHub
```bash
wget https://raw.githubusercontent.com/Lab-Brat/linux_scripts/main/ansible/app_forms.yaml
```
* add your host to the inventory file, and run the playbook 
```bash
ansible-playbook app_forms.yaml --limit <host>
```

#### Run
* Docker: It will run automatically, becuase it's defined in ```entry_point.sh```
* Ansible: After the deployment is complete, login to the server, navigate to the installation directory and run 
```bash
python app.py

# if the port is changed to 80 or 433
# sudo python app.py
```

#### Open
To open app interface, open a browser and enter server's IP address (or hostname) and port in the search bar, for example:
```
http://192.168.0.1:5000
```
