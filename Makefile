# Docker
COMPOSE          = docker-compose
COMPOSE_RUN      = $(COMPOSE) run --rm
COMPOSE_EXEC      = $(COMPOSE) exec

# Django
MANAGE_CMS       = $(COMPOSE_RUN) cms python manage.py cms
MANAGE_LMS       = $(COMPOSE_RUN) lms python manage.py lms

default: help

bootstrap: clone build run collectstatic migrate demo-course  ## install development dependencies

build:  ## build all containers
	@$(COMPOSE) build;
.PHONY: build

clone:  ## clone source repositories
	@./bin/clone_repositories;
.PHONY: clone

collectstatic:  ## copy static assets to static root directory
	$(COMPOSE_EXEC) lms-dev python manage.py lms collectstatic --noinput --settings=fun.docker_run_lms_staging;
	$(COMPOSE_EXEC) cms-dev python manage.py cms collectstatic --noinput --settings=fun.docker_run_cms_staging;
.PHONY: collectstatic

demo-course:  ## import demo course from edX repository
	@./bin/clone_demo_course
	$(COMPOSE_RUN) -v $(shell pwd)/src/edx-demo-course:/edx/app/edxapp/edx-demo-course cms \
	python manage.py cms import /edx/var/edxapp/media /edx/app/edxapp/edx-demo-course
.PHONY: demo-course

dev:  ## activate source overrides for development
	# Mount the edx-platform repository volume and synchronize the host with
	# the container so that we can see our changes immediately.
	@$(COMPOSE) up -d
	docker cp $(shell docker-compose ps -q lms-dev):/edx/app/edxapp/edx-platform src/
	docker cp $(shell docker-compose ps -q lms-dev):/edx/app/edxapp/fun-apps src/
	@$(COMPOSE) -f docker-compose.yml -f dev-volumes.yml up -d
.PHONY: dev

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

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
.PHONY: help
