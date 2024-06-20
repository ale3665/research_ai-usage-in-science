#!/bin/bash
source optparse.bash

optparse.define short=a long=author-input desc="A directory of OpenAlex Authors files to read" variable=authorInput

optparse.define short=b long=work-input desc="A directory of OpenAlex Works files to read" variable=workInput
source $( optparse.build )
