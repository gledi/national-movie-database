.PHONY: check list outdated tools compile sync prepare-run run cleanup-run image image-prod build up down destroy ps top start stop logs shell djshell test

SHELL := /bin/bash

cache = 1

PY_VERSION = 3.11.1
PYENV_PREFIX = $(shell ~/.pyenv/bin/pyenv prefix $(PY_VERSION))
PYENV_PYTHON_BIN = $(PYENV_PREFIX)/bin/python
PYTHON = ./venv/bin/python
REPOSITORY = gledi/nmdb
TAG = develop
SVC = web
REQUIREMENTS = dev
CMD = bash

ifeq ($(cache), 0)
	NO_CACHE = --no-cache
endif


check:
	@echo "PY_VERSION =" $(PY_VERSION)
	@echo "PYENV_PREFIX =" $(PYENV_PREFIX)
	@echo "PYENV_PYTHON_BIN =" $(PYENV_PYTHON_BIN)
	@echo "REPOSITORY =" $(REPOSITORY)
	@echo "TAG =" $(TAG)
	@echo "SVC =" $(SVC)
	@echo "CMD =" $(CMD)
	@echo "NO_CACHE =" $(NO_CACHE)
	@echo "REQUIREMENTS =" $(REQUIREMENTS)

venv:
	@echo "Virtual environment does not exist. Creating it now ..."
	$(PYENV_PYTHON_BIN) -m venv --prompt=nmdb venv

list: | venv
	$(PYTHON) -m pip list

outdated: | venv
	$(PYTHON) -m pip list --outdated

tools: | venv
	$(PYTHON) -m pip install --upgrade --upgrade-strategy=eager pip setuptools wheel pip-tools

compile: tools
	$(PYTHON) -m piptools compile --resolver=backtracking --upgrade --output-file requirements/main.txt
	$(PYTHON) -m piptools compile --resolver=backtracking --upgrade --extra=test --output-file requirements/test.txt
	$(PYTHON) -m piptools compile --resolver=backtracking --upgrade --extra=prod --output-file requirements/prod.txt
	$(PYTHON) -m piptools compile --resolver=backtracking --upgrade --all-extras --output-file requirements/dev.txt

sync: tools
	$(PYTHON) -m piptools sync requirements/$(REQUIREMENTS).txt

prepare-run:
	if [[ "$(shell docker ps -aq --filter name=nmdb-cache)" != "" ]]; then docker rm -f nmdb-cache; fi
	if [[ "$(shell docker ps -aq --filter name=nmdb-db)" != "" ]]; then docker rm -f nmdb-db; fi
	if [[ "$(shell docker volume ls --filter name=nmdb_l_dbdata)" == "" ]]; then docker volume create nmdb_prepare_dbdata; fi
	@docker run --rm --name=nmdb-cache -p 26379:6379 -d redis:alpine
	@docker run --rm --name=nmdb-db -p 25432:5432 -v nmdb_prepare_dbdata:/var/lib/postgresql/data -e PGTZ=UTC -e POSTGRES_DB=moviesdb -e POSTGRES_USER=movie -e POSTGRES_PASSWORD=star -d postgres:15-alpine

run:
	@source .env.sh && $(PYTHON) nmdb/manage.py runserver

cleanup-run:
	@docker stop nmdb-cache nmdb-db

image:
	@docker build --tag $(REPOSITORY):$(TAG) --force-rm $(NO_CACHE) .

image-prod:
	@docker build --tag $(REPOSITORY):prod --tag $(REPOSITORY):latest --force-rm $(NO_CACHE) .

build:
	@docker compose build $(NO_CACHE)

up:
	@docker compose up --build -d

down:
	@docker compose down --remove-orphans --rmi local

destroy:
	@docker compose down --remove-orphans --rmi local --volumes

ps:
	@docker compose ps

top:
	@docker compose top $(SVC)

start:
	@docker compose start $(SVC)

stop:
	@docker compose stop $(SVC)

logs:
	@docker compose logs -f $(SVC)

shell:
	@docker compose exec $(SVC) $(CMD)

djshell:
	@docker compose exec web python manage.py shell_plus

test:
	@docker compose run --rm web python -m pytest -v
