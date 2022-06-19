#!/bin/bash

docker run --name masque_db \
	   --net masque_network \
	   -e POSTGRES_USER=boink \
	   -e POSTGRES_PASSWORD=password \
	   -e POSTGRES_DB=masq_forms \
	   -d postgres

