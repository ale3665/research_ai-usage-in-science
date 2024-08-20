#!/bin/bash

source optparse.bash

optparse.define short=d long=date desc="Optional date value to leverage pre-computed results" variable=DATE default=$(date +"%m-%d-%Y")

source $( optparse.build )

DATA_PATH="./data/"

# 1. Search through journal
python3.10 getData_plos.py --output $DATA_PATH/searchResponse_plos_$DATE.json
