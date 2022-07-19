#!/bin/bash

export DB_USER=postgres
export DB_PASS=password
export DB_ADDRESS=127.0.0.1
export DB_PORT=5432
export DB_NAME=masq_forms


db_user=$DB_USER
db_name=$DB_NAME
db_address=$DB_ADDRESS
db_port=$DB_PORT

form_columns="(name, hostname, unit_belong, ip, distro, functions, subsystems, date_created)"
exip_columns="(forms_id, extra_ip)"
unit_columns="(unit_name, unit_level, description, cluster, containerization, pod, unit_functions, unit_subsystems, date_created)"
form_entries="./form_entries.csv"
exip_entries="./exip_entries.csv"
unit_entries="./unit_entries.csv"

psql -U $db_user \
     -d $db_name \
     -h $db_address \
     -p $db_port \
     -c "\copy forms $form_columns from $form_entries with DELIMITER ','" \
     -c "\copy extra_ips $exip_columns from $exip_entries with DELIMITER ','" \
     -c "\copy units_forms $unit_columns from $unit_entries with DELIMITER ','"

echo "============= Database Populated ============="
