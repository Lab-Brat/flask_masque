#!/bin/bash

export DB_USER=labbrat
#export DB_PASS=password
export DB_ADDRESS='127.0.0.1'
export DB_PORT=5433
export DB_NAME=masq_forms

export DB_URI="postgresql://$DB_USER@$DB_ADDRESS:$DB_PORT/$DB_NAME"

