# Get local user ids
UID              = $(shell id -u)
GID              = $(shell id -g)

# Docker
COMPOSE          = UID=$(UID) GID=$(GID) docker-compose
COMPOSE_RUN      = $(COMPOSE) run --rm -e HOME="/tmp"
COMPOSE_EXEC     = $(COMPOSE) exec

# Django
MANAGE_CMS       = $(COMPOSE_RUN) cms python manage.py cms
MANAGE_LMS       = $(COMPOSE_RUN) lms python manage.py lms

default: help

bootstrap: tree clone run collectstatic migrate demo-course  ## install development dependencies

# Build production image. Note that the cms service uses the same image built
# for the lms service.
build:  ## build the edxapp production image
	@echo "🐳 Building production image..."
	$(COMPOSE) build lms
.PHONY: build

# Build development image. Note that the cms-dev service uses the same image
# built for the lms-dev service.
build-dev:  ## build the edxapp production image
	@echo "🐳 Building development image..."
	$(COMPOSE) build lms-dev
.PHONY: build

clone:  ## clone source repositories
	@./bin/clone_repositories;
.PHONY: clone

collectstatic: tree  ## copy static assets to static root directory
	$(COMPOSE_RUN) lms python manage.py lms collectstatic --noinput --settings=fun.docker_run;
	$(COMPOSE_RUN) cms python manage.py cms collectstatic --noinput --settings=fun.docker_run;
.PHONY: collectstatic

create-symlinks:  ## create symlinks to local configuration (mounted via a volume)
	$(COMPOSE_RUN) --no-deps lms-dev bash -c "\
		rm -f /edx/app/edxapp/edx-platform/lms/envs/fun && \
		rm -f /edx/app/edxapp/edx-platform/cms/envs/fun && \
		ln -sf /config/lms /edx/app/edxapp/edx-platform/lms/envs/fun && \
		ln -sf /config/cms /edx/app/edxapp/edx-platform/cms/envs/fun"
.PHONY: create-symlinks

demo-course: tree  ## import demo course from edX repository
	@./bin/clone_demo_course
	$(COMPOSE_RUN) -v $(shell pwd)/src/edx-demo-course:/edx/app/edxapp/edx-demo-course cms \
	python manage.py cms import /edx/var/edxapp/data /edx/app/edxapp/edx-demo-course
.PHONY: demo-course

# In development, we work with local directories (on our host machine) for
# static files and for edx-platform sources, and mount them in the container
# (using Docker volumes). Hence, you will need to run the update_assets target
# everytime you update edx-platform sources and plan to develop in it.
update-assets: tree create-symlinks  ## run update_assets to copy required statics in local volumes
	$(COMPOSE_RUN) --no-deps lms-dev \
		paver update_assets --settings=fun.docker_build_development --skip-collect
.PHONY: update-assets

# As we mount edx-platform as a volume in development, we need to re-create
# symlinks that points to our custom configuration
dev: tree create-symlinks  ## start the cms and lms services (development image and servers)
	$(COMPOSE) up -d cms-dev  # starts lms-dev as well via dependency
.PHONY: dev

watch-assets: tree  ## start assets watcher (front-end development)
	$(COMPOSE_EXEC) lms-dev \
		paver watch_assets --settings=fun.docker_build_development

logs:  ## get development logs
	$(COMPOSE) logs -f
.PHONY: logs

migrate:  ## perform database migrations
	$(MANAGE_LMS) migrate;
	$(MANAGE_CMS) migrate;
.PHONY: migrate

run: tree  ## start the cms and lms services (nginx + production image)
	$(COMPOSE) up -d nginx
.PHONY: run

stop:  ## stop the development servers
	$(COMPOSE) stop
.PHONY: stop

superuser:  ## create a super user
	$(MANAGE_LMS) createsuperuser
.PHONY: superuser

tree:  ## create data directories mounted as volumes
	bash -c "mkdir -p data/{static/production,static/development,media,store}"
.PHONY: tree

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
.PHONY: help
