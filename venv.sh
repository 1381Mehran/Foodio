#!/bin/bash

ENV_NAME=venv

python3 -m venv $ENV_NAME

cd $ENV_NAME/bin

source ./activate

cd ../..

