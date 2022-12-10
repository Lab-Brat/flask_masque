#!/bin/bash

DB_USER="labbrat"
DB_NAME="masq_forms"
DB_ADDRESS="127.0.0.1"
DB_PORT=5432

form_columns="(name, hostname, unit_belong, ip, distro, functions, subsystems, date_created)"
exip_columns="(forms_id, extra_ip)"
unit_columns="(unit_name, unit_level, description, cluster, containerization, pod, unit_functions, unit_subsystems, date_created)"
form_entries="./form_entries.csv"
exip_entries="./exip_entries.csv"
unit_entries="./unit_entries.csv"

psql -U $DB_USER \
     -d $DB_NAME \
     -h $DB_ADDRESS \
     -p $DB_PORT \
     -c "\copy forms $form_columns from $form_entries with DELIMITER ','" \
     -c "\copy extra_ips $exip_columns from $exip_entries with DELIMITER ','" \
     -c "\copy units_forms $unit_columns from $unit_entries with DELIMITER ','"

echo "============= Database Populated ============="
