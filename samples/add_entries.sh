#!/bin/bash

columns="(name, hostname, ip, distro, functions, subsystems, date_created)"
entries="~/github/flask_masque/samples/entries.csv"

psql -U labbrat \
     -d masq_forms \
     -h localhost \
     -p 5433 \
     -c "\copy forms $columns from $entries with DELIMITER ','"

