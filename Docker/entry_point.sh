#!/bin/bash
[ ! -d "./migrations" ] && flask db init
flask db stamp head
flask db migrate
flask db upgrade

flask run --host=0.0.0.0
