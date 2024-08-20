#!/bin/bash

source optparse.bash

optparse.define short=d long=date desc="Optional date value to leverage pre-computed results" variable=DATE default=$(date +"%m-%d-%Y")

source $( optparse.build )

DATA_PATH="./data/"

# 1. Search through journal
python3.10 getData_plos.py \
    --output $DATA_PATH/searchResponse_plos_$DATE.json

# 2. Filter data
python3.10 filterData_plos.py \
    --input $DATA_PATH/searchResponse_plos_$DATE.json \
    --sample-output $DATA_PATH/sampled_searchResponse_plos_$DATE.json \
    --filter-output $DATA_PATH/filter_sampled_searchResponse_plos_$DATE.json \
    --sample-frac 0.5

# 3. Open data
python3.10 openSamples.py \
    --input $DATA_PATH/filter_sampled_searchResponse_plos_$DATE.json

# 4. Plot data
python3.10 plot.py \
    --input $DATA_PATH/filter_sampled_searchResponse_plos_$DATE.json \
    --output $DATA_PATH/filter_sampled_searchResponse_plot_plos_$DATE.png \
