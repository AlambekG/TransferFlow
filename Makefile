PYTHON=python
PIP=$(PYTHON) -m pip

.PHONY: install test build docker-build

install:
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt -r requirements-dev.txt

test: install
	pytest

build:
	docker build -t transferflow-api:local .

docker-build: build
