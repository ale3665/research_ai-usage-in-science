#!/bin/bash
DATE=$(date +"%m-%d-%Y")

aius-search --journal plos --output ../data/plos/search_$DATE.parquet
