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
docker-compose -f Docker/docker-compose.yml up
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
