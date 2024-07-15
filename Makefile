build:
	poetry build
	pip install dist/*.tar.gz

build-docs:
	sphinx-build --builder html src-docs build-docs

create-dev:
	rm -rf env
	python3.10 -m venv env
	( \
		. env/bin/activate; \
		pip install -r requirements.txt; \
		poetry install; \
		deactivate; \
	)

create-docs:
	sphinx-apidoc src --output-dir src-docs --maxdepth 100 --separate

create-output-dir:
	mkdir -p data/nature
	mkdir -p data/plos
	mkdir -p data/science

	mkdir -p data/nature/zettels
	mkdir -p data/plos/zettels
	mkdir -p data/science/zettels
