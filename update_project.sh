#!/bin/bash

branch_name=$1

if [[ -z "$branch_name" ]]
then

  echo

  echo "invalid Branch name"

  echo

else

  git pull origin "$branch_name" --rebase

  docker compose -f docker-compose-persistent.yml -f docker-compose.yml down

  docker build -f Dockerfile -t foodio:latest .

  docker compose -f docker-compose-persistent.yml -f docker-compose.yml up

fi
