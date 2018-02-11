# Docker
COMPOSE          = docker-compose
COMPOSE_RUN      = $(COMPOSE) run --rm
COMPOSE_RUN_CMS  = $(COMPOSE_RUN) cms
COMPOSE_RUN_LMS  = $(COMPOSE_RUN) lms

# Django
MANAGE_CMS       = $(COMPOSE_RUN_CMS) python manage.py cms
MANAGE_LMS       = $(COMPOSE_RUN_LMS) python manage.py lms

default: help

bootstrap: clone build run update-assets migrate demo-course  ## install development dependencies

build:  ## build all containers
	@$(COMPOSE) build;
	# Mount the edx-platform repository volume and reinstall the requirements that
	# modify it so the project will also work with sources mounted on the host for
	# development.
	@$(COMPOSE_RUN_LMS) bash -c "\
	pip install --src ../src -r requirements/edx/local.txt && npm install && \
	cd /app/edx-platform/node_modules/edx-ui-toolkit && npm install"
.PHONY: build

clone:  ## clone source repositories
	@./bin/clone_repositories;
.PHONY: clone

demo-course:  ## import demo course from edX repository
	@./bin/clone_demo_course
	docker-compose run --rm -v $(shell pwd)/src/edx-demo-course:/app/edx-demo-course cms \
	python manage.py cms --settings=fun_platform import /data/media /app/edx-demo-course
.PHONY: demo-course

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

superuser:  ## create a super user
	@$(MANAGE_LMS) createsuperuser
.PHONY: superuser

update-assets:  ## build front-end application
	$(COMPOSE) exec cms paver update_assets cms --settings=production;
	$(COMPOSE) exec lms paver update_assets lms --settings=production;
.PHONY: update-assets

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
.PHONY: help
