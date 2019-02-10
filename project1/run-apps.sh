#!/bin/bash

# start mysql service
service mysql start

# run our app
python3 -B /project1/apps/app.py

# keep container running
# while :; do
#   sleep 300
# done