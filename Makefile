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

pipeline:
	aius-search -j nature -o nature_search.pickle
	aius-search -j plos -o plos_search.pickle
	aius-search -j science -o science_search.pickle
