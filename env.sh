#!/bin/bash

export DB_USER=boink
export DB_PASS=password
export DB_ADDRESS=flask_masque_masq_db_1
export DB_PORT=5432
export DB_NAME=masq_forms

export DB_URI="postgresql://$DB_USER:$DB_PASS@$DB_ADDRESS:$DB_PORT/$DB_NAME"
