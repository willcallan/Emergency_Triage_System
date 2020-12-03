#!/bin/bash

docker stop $(docker ps -aq)

cd app/front-end
docker build --tag edts-frontend:latest .
cd -

cp .localenv app/back-end/.env
cd app/back-end
docker build --tag edts-api:latest .
cd -

cd app/db
docker build --tag edts-db:latest .
cd -

