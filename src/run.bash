#!/bin/bash
DATE=$(date +"%m-%d-%Y")

# Step 1: Search for documents within mega journals
aius-search --journal plos --output ../data/plos/search_$DATE.parquet

# Step 2: Filter for papers indexed in OpenAlex
