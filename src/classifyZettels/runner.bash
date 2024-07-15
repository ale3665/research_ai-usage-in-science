#!/bin/bash

python main.py -i ../../data/plos/zg.db -c nature-subjects -m llama3
python main.py -i ../../data/plos/zg.db -c nature-topics -m llama3
python main.py -i ../../data/plos/zg.db -c scopus-subjects -m llama3
python main.py -i ../../data/plos/zg.db -c scopus-topics -m llama3

python main.py -i ../../data/plos/zg.db -c nature-subjects -m gemma
python main.py -i ../../data/plos/zg.db -c nature-topics -m gemma
python main.py -i ../../data/plos/zg.db -c scopus-subjects -m gemma
python main.py -i ../../data/plos/zg.db -c scopus-topics -m gemma

python main.py -i ../../data/plos/zg.db -c nature-subjects -m gemma2
python main.py -i ../../data/plos/zg.db -c nature-topics -m gemma2
python main.py -i ../../data/plos/zg.db -c scopus-subjects -m gemma2
python main.py -i ../../data/plos/zg.db -c scopus-topics -m gemma2
