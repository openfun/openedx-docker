# Docker
COMPOSE          = docker-compose
COMPOSE_RUN      = $(COMPOSE) run --rm
COMPOSE_RUN_CMS  = $(COMPOSE_RUN) cms
COMPOSE_RUN_LMS  = $(COMPOSE_RUN) lms

# Django
MANAGE_CMS       = $(COMPOSE_RUN_CMS) python manage.py cms
MANAGE_LMS       = $(COMPOSE_RUN_LMS) python manage.py lms

default: help


bootstrap: build run update-assets migrate  ## install development dependencies

build:  ## build all containers
	@$(COMPOSE) build;
.PHONY: build

logs:  ## get development logs
	@$(COMPOSE) logs -f
.PHONY: logs

migrate:  ## perform database migrations
	@$(MANAGE_LMS) migrate;
	@$(MANAGE_CMS) migrate;
.PHONY: migrate

run:  ## start the development servers
	@$(COMPOSE) up -d
.PHONY: run

stop:  ## stop the development servers
	@$(COMPOSE) stop
.PHONY: stop

update-assets:  ## build front-end application
	$(COMPOSE) exec cms paver update_assets cms --settings=production;
	$(COMPOSE) exec lms paver update_assets lms --settings=production;
.PHONY: update-assets

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
.PHONY: help

