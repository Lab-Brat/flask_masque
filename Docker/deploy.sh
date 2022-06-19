#!/bin/bash
docker network create masque_network
docker image build -t flask_docker -f Docker/Dockerfile .

docker run --name masque_db \
		   --net masque_network \
		   -e POSTGRES_USER=boink \
		   -e POSTGRES_PASSWORD=password \
		   -e POSTGRES_DB=masq_forms \
		   -d postgres

docker run --name app_container \
           --net masque_network \
		   -p 5000:5000  \
           -d flask_docker
