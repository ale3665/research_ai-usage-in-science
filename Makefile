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
