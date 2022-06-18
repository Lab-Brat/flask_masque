#!/bin/bash

db_user=$(grep 'db_user' ../config.ini | cut -d" " -f3 | tr -d $'\r')
db_name=$(grep 'db_name' ../config.ini | cut -d" " -f3 | tr -d $'\r')
db_address=$(grep 'db_address' ../config.ini | cut -d" " -f3 | tr -d $'\r')
db_port=$(grep 'db_port' ../config.ini | cut -d" " -f3 | tr -d $'\r')
db_entries=$(grep 'sample_entries' ../config.ini | awk '{print $3}' | tr -d $'\r')
db_columns="(name, hostname, ip, distro, functions, subsystems, date_created)"


psql -U $db_user \
     -d $db_name \
     -h $db_address \
     -p $db_port \
     -c "\copy forms $db_columns from $db_entries with DELIMITER ','"
