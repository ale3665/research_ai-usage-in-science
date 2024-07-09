#!/bin/bash
source optparse.bash

# Search through journals flags
optparse.define short=a long=nature-search-result-output desc="Path to save Nature search results to" variable=natureSearchResultOutput
optparse.define short=b long=plos-search-result-output desc="Path to save PLOS search results to" variable=plosSearchResultOutput



source $( optparse.build )

# Convert relative paths to absolute paths
nsro=$(realpath $natureSearchResultOutput)
psro=$(realpath $plosSearchResultOutput)
ssro=$(realpath $scienceSearchResultOutput)

# Search through journals
aius-search -j nature -o $nsro
aius-search -j plos -o $psro

# Download papers
