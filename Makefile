.DEFAULT_GOAL := help

SHELL := /bin/bash

PROJECTNAME := $(shell basename $(CURDIR))
PACKAGE_NAME := national-movie-database

PY_VER := 3.13
VENV_DIR := $(CURDIR)/.venv
VENV_PROMPT := nmdb

PY := $(VENV_DIR)/bin/python
UV := $(shell which uv 2>/dev/null || echo "uv")

IMAGE_NAME := gledi/nmdb
PLATFORM := linux/amd64

CMD := /bin/bash
SVC := web


.PHONY: help print-%
.SILENT: help print-%

##@ Meta
help: ## Show this help message and exit
	echo ""
	echo "Manage $(PROJECTNAME). Usage:"
	awk 'BEGIN{FS=":.*##"} \
	     /^##@/{printf "\n\033[1m%s\033[0m\n",substr($$0,5);next} \
	     /^[a-zA-Z0-9_%\/. -]+:.*##/{gsub(/ /,"|",$$1);printf "  \033[36m%-24s\033[0m %s\n",$$1,$$2}' $(MAKEFILE_LIST)
	echo ""

print-%: ## Print the value of a variable (e.g. make print-PY_VER)
	@echo $* = $($*)


.PHONY: venv list outdated lock lock/check relock sync sync/dry deps deps/outdated why dev dev/up
.SILENT: venv

##@ Environment & dependencies
venv: ## Create a virtual environment
	if ! [[ -d $(VENV_DIR) ]]; then \
		$(UV) venv --no-project --seed --link-mode=copy --prompt=$(VENV_PROMPT) $(VENV_DIR) --python=$(PY_VER); \
	else \
		echo "Virtual environment already exists"; \
	fi

list: ## List all dependencies
	$(UV) pip list

outdated: ## List outdated dependencies
	$(UV) pip list --outdated

lock: ## Lock dependencies (uv lock --upgrade)
	$(UV) lock --upgrade

lock/check: ## Check lockfile is up-to-date
	$(UV) lock --check

relock: ## Re-lock after pyproject edits WITHOUT upgrading deps (uv lock)
	$(UV) lock

sync: ## Sync dependencies from lockfile
	$(UV) sync --locked --all-extras --all-groups --link-mode=copy

sync/dry: ## Dry run of syncing dependencies from lockfile
	$(UV) sync --locked --all-extras --all-groups --link-mode=copy --dry-run

deps: ## Show dependency tree
	$(UV) tree

deps/outdated: ## Show dependency tree with outdated packages highlighted
	$(UV) tree --outdated

why: ## Show why a package is installed: make why <package>
	@test -n "$(filter-out $@,$(MAKECMDGOALS))" || { echo "usage: make why <package>"; exit 1; }
	$(UV) tree --invert --package "$(filter-out $@,$(MAKECMDGOALS))"

dev: venv relock sync ## Create venv, lock deps, and sync them

dev/up: venv lock sync ## Create venv, lock with upgrade, and sync deps


.PHONY: version build clean
.SILENT: version clean

##@ Build
version: ## Show Python, uv and package versions
	$(UV) run --locked python --version
	$(UV) --version

build: ## Build the package
	$(UV) build

clean: ## Remove build artifacts and caches
	rm -rf dist/ build/
	rm -rf .pytest_cache/ .ruff_cache/
	find . -path ./.venv -prune -o -type d -name '*.egg-info' -print -exec rm -rf {} +
	find . -path ./.venv -prune -o -type d -name __pycache__ -print -exec rm -rf {} +


.PHONY: run djshell

##@ Run locally
run: ## Run the django development server locally
	$(UV) run --locked nmdb runserver

djshell: ## Enter the django shell locally
	$(UV) run --locked nmdb shell_plus


.PHONY: img img-dev up up/build down ps top stats start stop restart logs sh

##@ Docker images
img: ## Build production Docker image
	docker build --platform $(PLATFORM) --tag $(IMAGE_NAME):latest --tag $(IMAGE_NAME):prod --force-rm .

img-dev: ## Build development Docker image
	docker build --platform $(PLATFORM) --tag $(IMAGE_NAME):dev --force-rm .


##@ Compose stack
up: ## Run all services
	docker compose up --build -d

up/build: ## Rebuild and run all services
	docker compose up --build -d --force-recreate

down: ## Stop and remove all services
	docker compose down --remove-orphans

ps: ## Show services and their status
	docker compose ps --all

top: ## Show running processes for containers
	docker compose top $(SVC)

stats: ## Show resource usage statistics for containers
	docker compose stats

start: ## Start services (all if none specified)
	docker compose start $(if $(filter-out $@,$(MAKECMDGOALS)), $(filter-out $@,$(MAKECMDGOALS)),)

stop: ## Stop services (all if none specified)
	docker compose stop $(if $(filter-out $@,$(MAKECMDGOALS)), $(filter-out $@,$(MAKECMDGOALS)),)

restart: ## Restart services (all if none specified)
	docker compose restart $(if $(filter-out $@,$(MAKECMDGOALS)), $(filter-out $@,$(MAKECMDGOALS)),)

logs: ## Show logs for a service (default: web)
	docker compose logs -f $(if $(filter-out $@,$(MAKECMDGOALS)), $(filter-out $@,$(MAKECMDGOALS)), $(SVC))

sh: ## Run command in service (default: web, command: /bin/bash)
	docker compose exec $(if $(filter-out $@,$(MAKECMDGOALS)), $(filter-out $@,$(MAKECMDGOALS)), $(SVC)) $(CMD)


.PHONY: test cov cov/report
.SILENT: cov/report

##@ Test
test: ## Run tests
	$(UV) run --locked pytest --no-cov

cov: ## Run tests with coverage
	$(UV) run --locked pytest --cov=nmdb

cov/report: ## Generate coverage reports (html, xml, terminal)
	$(UV) run --locked coverage report
	$(UV) run --locked coverage html


.PHONY: lint/check lint/fix fmt/check fmt/fix

##@ Lint & format
lint/check: ## Check for linting issues (ruff check)
	$(UV) run --locked ruff check src/ tests/

lint/fix: ## Fix linting issues (ruff check --fix)
	$(UV) run --locked ruff check --fix src/ tests/

fmt/check: ## Check for formatting issues (ruff format --check)
	$(UV) run --locked ruff format --check src/ tests/

fmt/fix: ## Fix formatting issues (ruff format)
	$(UV) run --locked ruff format src/ tests/


%:
	@:
