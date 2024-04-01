#!/bin/bash

ENV_NAME=venv

ls /app

python3 -m venv $ENV_NAME

cd $ENV_NAME/bin


./activate

cd ../..

