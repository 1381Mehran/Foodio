#!/bin/bash

git pull origin $1 --rebase

#docker compose -f docker-compose-persistent.yml -f docker-compose.yml down

docker build -f Dockerfile -t foodio:latest .

docker compose -f docker-compose-persistent.yml -f docker-compose.yml up

