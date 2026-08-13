PYTHON=python
PIP=$(PYTHON) -m pip

.PHONY: install test build docker-build

help:
	@echo "Makefile commands:"
	@echo "  make install       Install runtime and dev dependencies"
	@echo "  make test          Run test suite"
	@echo "  make build         Build Docker image (local)"
	@echo "  make docker-build  Alias for build"


install:
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt -r requirements-dev.txt

test: install
	pytest

build:
	docker build -t transferflow-api:local .

docker-build: build
