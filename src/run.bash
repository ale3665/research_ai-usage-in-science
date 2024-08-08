#!/bin/bash
DATE=$(date +"%m-%d-%Y")
PLOS_PATH="../data/plos"

# Step 1: Search for documents within mega journals
aius-search --journal plos --output $PLOS_PATH/search_$DATE.parquet

# Step 2: Plot search result statistics
aius-search-plot --input $PLOS_PATH/search_$DATE.parquet --fig-1 $PLOS_PATH/searchResultPagesPerYear.png --fig-2 $PLOS_PATH/searchResultPagesPerQuery.png

# Step 3: Filter for papers indexed in OpenAlex
