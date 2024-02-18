.PHONY: help info \
	venv list outdated tools compile sync install install-dev dev run \
	img img-dev build up down ps top start stop logs shell djshell test

.SILENT: help info venv

.DEFAULT_GOAL := help

PY_VERSION := 3.13
PYENV_PREFIX := $(shell pyenv prefix $(PY_VERSION))
PYENV_PYTHON_BIN := $(PYENV_PREFIX)/bin/python
VENV_DIR := $(CURDIR)/.venv
VENV_PROMPT := nmdb
PY := $(VENV_DIR)/bin/python
REPOSITORY := gledi/nmdb
PLATFORM := linux/amd64


help:
	echo "Usage: make [target]"
	echo "Targets:"
	echo "  help: Show this help message"
	echo "  info: Show information on variables used in this makefile"

info:
	echo "PY_VERSION =" $(PY_VERSION)
	echo "PYENV_PREFIX =" $(PYENV_PREFIX)
	echo "PYENV_PYTHON_BIN =" $(PYENV_PYTHON_BIN)
	echo "VENV_DIR =" $(VENV_DIR)
	echo "PY =" $(PY)
	echo "REPOSITORY =" $(REPOSITORY)
	echo "PLATFORM =" $(PLATFORM)

venv:
	if ! [[ -d $(VENV_DIR) ]]; then $(PYENV_PYTHON_BIN) -m venv --prompt=$(VENV_PROMPT) $(VENV_DIR); else echo "$(VENV_DIR) already exists. skipping ..."; fi

list:
	$(PY) -m pip list

outdated:
	$(PY) -m pip list --outdated

tools:
	$(PY) -m pip install --upgrade --upgrade-strategy=eager pip pip-tools

compile:
	$(PY) -m piptools compile --annotation-style=line --resolver=backtracking --upgrade --extra=prod --output-file requirements/prod.txt
	$(PY) -m piptools compile --annotation-style=line --resolver=backtracking --upgrade --all-extras --output-file requirements/dev.txt

sync:
	$(PY) -m piptools sync requirements/dev.txt

install:
	$(PY) -m pip install --no-deps .

install-dev:
	$(PY) -m pip install --no-deps --editable '.[prod,test,dev]'

dev: tools compile sync install-dev

run:
	nmdb runserver

img:
	docker build --platform $(PLATFORM) --tag $(REPOSITORY):latest --tag $(REPOSITORY):prod --force-rm .

img-dev:
	docker build --platform $(PLATFORM) --tag $(REPOSITORY):dev --force-rm .

build:
	docker compose build

up:
	docker compose up --build -d

down:
	docker compose down --remove-orphans --rmi local

ps:
	docker compose ps

top:
	docker compose top $(SVC)

start:
	docker compose start $(SVC)

stop:
	docker compose stop $(SVC)

logs:
	docker compose logs -f $(SVC)

shell:
	docker compose exec $(SVC) $(CMD)

djshell:
	docker compose exec web python manage.py shell_plus

test:
	docker compose run --rm web python -m pytest -v
