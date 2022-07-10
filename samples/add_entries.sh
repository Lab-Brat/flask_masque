#!/bin/bash

db_user=$(grep 'db_user' ../config.ini | cut -d" " -f3 | tr -d $'\r')
db_name=$(grep 'db_name' ../config.ini | cut -d" " -f3 | tr -d $'\r')
db_address=$(grep 'db_address' ../config.ini | cut -d" " -f3 | tr -d $'\r')
db_port=$(grep 'db_port' ../config.ini | cut -d" " -f3 | tr -d $'\r')

form_columns="(name, hostname, unit_belong, ip, distro, functions, subsystems, date_created)"
exip_columns="(forms_id, extra_ip)"
unit_columns="(unit_name, unit_level, description, cluster, containerization, pod, unit_functions, unit_subsystems, date_created)"
sample_path=$(grep 'sample_path' ../config.ini | awk '{print $3}' | tr -d $'\r')
form_entries="$sample_path/form_entries.csv"
exip_entries="$sample_path/exip_entries.csv"
unit_entries="$sample_path/unit_entries.csv"

psql -U $db_user \
     -d $db_name \
     -h $db_address \
     -p $db_port \
     -c "\copy forms $form_columns from $form_entries with DELIMITER ','" \
     -c "\copy extra_ips $exip_columns from $exip_entries with DELIMITER ','" \
     -c "\copy units_forms $unit_columns from $unit_entries with DELIMITER ','"

echo "============= Database Populated ============="
