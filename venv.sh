#!/bin/bash

ENV_NAME=venv

ls /app

python3 -m venv /app/$ENV_NAME

cd $ENV_NAME/bin

source ./activate

cd ../..

