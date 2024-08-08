#!/bin/bash
DATE=$(date +"%m-%d-%Y")

# Step 1: Search for documents within mega journals
aius-search --journal plos --output ../data/plos/search_$DATE.parquet

# Step 2: Plot search result statistics
aius-search-plot --input ../data/plos/search_$DATE.parquet --fig-1 ../data/plos/plos_searchResultPagesPerYear.png --fig-2 ../data/plos/plos_searchResultPagesPerQuery.png


# Step 2: Filter for papers indexed in OpenAlex
