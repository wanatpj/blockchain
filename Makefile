SHELL := /bin/bash

create-venv-release:
	python3 -m venv venv/release
	source venv/release/bin/activate && pip install -e .

create-venv-dev:
	python3 -m venv venv/dev
	source venv/dev/bin/activate && pip install -r requirements/requirements-dev.txt && pip install -e .

delete-venv:
	rm -rf venv

show-activate-release:
	source venv/release/bin/activate

show-activate-dev:
	source venv/dev/bin/activate
