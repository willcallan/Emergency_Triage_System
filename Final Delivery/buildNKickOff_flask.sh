#!/usr/bin/bash

DOCKER_NAME=edts-flask
VERSION=1.1

if [ -e back-end ]; then
  rm -rf back-end
fi
cp -r ../../back-end .

docker stop $DOCKER_NAME
docker rm $DOCKER_NAME

docker build -t $DOCKER_NAME:$VERSION .
docker create --name $DOCKER_NAME -P -t -p 5000:5000 $DOCKER_NAME:$VERSION
docker start $DOCKER_NAME
