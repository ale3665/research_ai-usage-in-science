build:
	poetry build
	pip install dist/*.tar.gz

create-dev:
	rm -rf env
	python3.10 -m venv env
	( \
		. env/bin/activate; \
		pip install -r requirements.txt; \
		poetry install; \
		deactivate; \
	)

create-output-dir:
	mkdir -p data/nature/html/search
	mkdir -p data/nature/pickle/search

	mkdir -p data/plos/html/search
	mkdir -p data/plos/pickle/search

	mkdir -p data/science/html/search
	mkdir -p data/science/pickle/search

pipeline:
	aius-search -j nature -o data/nature/pickle/search/nature_search.pickle
	aius-search -j plos -o data/plos/pickle/search/plos_search.pickle
	aius-search -j science -o data/science/pickle/search/science_search.pickle

	aius-search-html-conversion -i data/nature/pickle/search/nature_search.pickle -o data/nature/html/search
	aius-search-html-conversion -i data/plos/pickle/search/plos_search.pickle -o data/plos/html/search
	aius-search-html-conversion -i data/science/pickle/search/science_search.pickle -o data/science/html/search
