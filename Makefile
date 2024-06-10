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
	aius-search -o nature_search.pickle --nature
	aius-search -o plos_search.pickle --plos
	aius-search -o science_search.pickle --science
