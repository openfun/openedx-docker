# Target OpenEdx release
EDX_RELEASE               ?= master
FLAVOR                    ?= bare
FLAVORED_EDX_RELEASE_PATH  = releases/$(shell echo ${EDX_RELEASE} | sed -r "s|\.|/|")/$(FLAVOR)
EDX_RELEASE_REF           ?= release-2018-08-29-14.14

# Target OpenEdx demo course release
EDX_DEMO_RELEASE_REF      ?= master

# Get local user ids
UID              = $(shell id -u)
GID              = $(shell id -g)

# Docker
COMPOSE          = \
  UID=$(UID) \
  GID=$(GID) \
  FLAVORED_EDX_RELEASE_PATH="$(FLAVORED_EDX_RELEASE_PATH)" \
  EDX_RELEASE_REF="$(EDX_RELEASE_REF)" \
  docker-compose
COMPOSE_RUN      = $(COMPOSE) run --rm -e HOME="/tmp"
COMPOSE_EXEC     = $(COMPOSE) exec

# Django
MANAGE_CMS       = $(COMPOSE_RUN) cms python manage.py cms
MANAGE_LMS       = $(COMPOSE_RUN) lms python manage.py lms

# Terminal colors
COLOR_DEFAULT = \033[0;39m
COLOR_ERROR   = \033[0;31m
COLOR_INFO    = \033[0;36m
COLOR_RESET   = \033[0m
COLOR_SUCCESS = \033[0;32m
COLOR_WARNING = \033[0;33m

default: help

# Target release expected tree
$(FLAVORED_EDX_RELEASE_PATH)/data/static/production/.keep:
	mkdir -p $(FLAVORED_EDX_RELEASE_PATH)/data/static/production
	touch $(FLAVORED_EDX_RELEASE_PATH)/data/static/production/.keep

$(FLAVORED_EDX_RELEASE_PATH)/data/static/development/.keep:
	mkdir -p $(FLAVORED_EDX_RELEASE_PATH)/data/static/development
	touch $(FLAVORED_EDX_RELEASE_PATH)/data/static/development/.keep

$(FLAVORED_EDX_RELEASE_PATH)/data/media/.keep:
	mkdir -p $(FLAVORED_EDX_RELEASE_PATH)/data/media
	touch $(FLAVORED_EDX_RELEASE_PATH)/data/media/.keep

$(FLAVORED_EDX_RELEASE_PATH)/data/store/.keep:
	mkdir -p $(FLAVORED_EDX_RELEASE_PATH)/data/store
	touch $(FLAVORED_EDX_RELEASE_PATH)/data/store/.keep

$(FLAVORED_EDX_RELEASE_PATH)/src/edx-demo-course/.keep:
	mkdir -p $(FLAVORED_EDX_RELEASE_PATH)/src/edx-demo-course
	touch $(FLAVORED_EDX_RELEASE_PATH)/src/edx-demo-course/.keep

$(FLAVORED_EDX_RELEASE_PATH)/src/edx-platform/.keep:
	mkdir -p $(FLAVORED_EDX_RELEASE_PATH)/src/edx-platform
	touch $(FLAVORED_EDX_RELEASE_PATH)/src/edx-platform/.keep

# We use this rule to prevent release archive download when it's already
# available. Note that this will also reset edx-platform sources (any changes
# will be discarded).
$(FLAVORED_EDX_RELEASE_PATH)/src/edx-platform/README.rst:
	rm -fr $(FLAVORED_EDX_RELEASE_PATH)/src/edx-platform
	${MAKE} $(FLAVORED_EDX_RELEASE_PATH)/src/edx-platform/.keep
	curl -Lo /tmp/edxapp.tgz https://github.com/edx/edx-platform/archive/$(EDX_RELEASE_REF).tar.gz
	tar xzf /tmp/edxapp.tgz -C $(FLAVORED_EDX_RELEASE_PATH)/src/edx-platform --strip-components=1

$(FLAVORED_EDX_RELEASE_PATH)/src/edx-demo-course/README.md:
	rm -fr $(FLAVORED_EDX_RELEASE_PATH)/src/edx-demo-course
	${MAKE} $(FLAVORED_EDX_RELEASE_PATH)/src/edx-demo-course/.keep
	curl -Lo /tmp/edx-demo.tgz https://github.com/edx/edx-demo-course/archive/$(EDX_DEMO_RELEASE_REF).tar.gz
	tar xzf /tmp/edx-demo.tgz -C $(FLAVORED_EDX_RELEASE_PATH)/src/edx-demo-course --strip-components=1

bootstrap: \
  tree \
  build \
  run \
  collectstatic \
  migrate \
  demo-course
bootstrap:  ## install development dependencies
.PHONY: bootstrap

# Build production image. Note that the cms service uses the same image built
# for the lms service.
build: \
  info \
  fetch-release
build:  ## build the edxapp production image
	@echo "🐳 Building production image..."
	$(COMPOSE) build lms
.PHONY: build

collectstatic: tree  ## copy static assets to static root directory
	$(COMPOSE_RUN) lms python manage.py lms collectstatic --noinput --settings=fun.docker_run
	$(COMPOSE_RUN) cms python manage.py cms collectstatic --noinput --settings=fun.docker_run
.PHONY: collectstatic

create-symlinks:  ## create symlinks to local configuration (mounted via a volume)
	$(COMPOSE_RUN) --no-deps lms-dev bash -c "\
		rm -f /edx/app/edxapp/edx-platform/lms/envs/fun && \
		rm -f /edx/app/edxapp/edx-platform/cms/envs/fun && \
		ln -sf /config/lms /edx/app/edxapp/edx-platform/lms/envs/fun && \
		ln -sf /config/cms /edx/app/edxapp/edx-platform/cms/envs/fun && \
		ln -sf /config/lms/root_urls.py /edx/app/edxapp/edx-platform/lms/"
.PHONY: create-symlinks

demo-course: \
  fetch-demo
demo-course:  ## import demo course from edX repository
	$(COMPOSE_RUN) -v $(PWD)/$(FLAVORED_EDX_RELEASE_PATH)/src/edx-demo-course:/edx/app/edxapp/edx-demo-course cms \
	python manage.py cms import /edx/var/edxapp/data /edx/app/edxapp/edx-demo-course
.PHONY: demo-course

# As we mount edx-platform as a volume in development, we need to re-create
# symlinks that points to our custom configuration
dev: \
  tree \
  create-symlinks
dev:  ## start the cms and lms services (development image and servers)
	# starts lms-dev as well via docker-compose dependency
	$(COMPOSE) up -d cms-dev
.PHONY: dev

# In development, we work with local directories (on our host machine) for
# static files and for edx-platform sources, and mount them in the container
# (using Docker volumes). Hence, you will need to run the update_assets target
# everytime you update edx-platform sources and plan to develop in it.
dev-assets: \
  tree \
  create-symlinks
dev-assets:  ## run update_assets to copy required statics in local volumes
	$(COMPOSE_RUN) --no-deps lms-dev \
		paver update_assets --settings=fun.docker_build_development --skip-collect
.PHONY: dev-assets

# Build development image. Note that the cms-dev service uses the same image
# built for the lms-dev service.
dev-build:  ## build the edxapp production image
	@echo "🐳 Building development image..."
	$(COMPOSE) build lms-dev
.PHONY: dev-build

dev-watch: \
  tree
dev-watch:  ## start assets watcher (front-end development)
	$(COMPOSE_EXEC) lms-dev \
		paver watch_assets --settings=fun.docker_build_development
.PHONY: dev-watch

# You can force archive download with the -B option:
#
#   $ make -B fetch-demo
fetch-demo: \
  $(FLAVORED_EDX_RELEASE_PATH)/src/edx-demo-course/README.md
fetch-demo:  ## fetch openedx demo course
	@echo "Demo course release '$(EDX_DEMO_RELEASE_REF)' is available at: $(FLAVORED_EDX_RELEASE_PATH)/src/edx-demo-course/"
.PHONY: fetch-demo

# You can force archive download with the -B option:
#
#   $ make -B fetch-release
fetch-release: \
  $(FLAVORED_EDX_RELEASE_PATH)/src/edx-platform/README.rst
fetch-release:  ## fetch openedx release sources
	@echo "Release '$(EDX_RELEASE_REF)' is available at: $(FLAVORED_EDX_RELEASE_PATH)/src/edx-platform/"
.PHONY: fetch-release

info:  ## get activated release info
	@echo "\n.:: OPENEDX-DOCKER ::.\n"
	@echo "== Active configuration ==\n"
	@echo "* EDX_RELEASE                : $(COLOR_INFO)$(EDX_RELEASE)$(COLOR_RESET)"
	@echo "* FLAVOR                     : $(COLOR_INFO)$(FLAVOR)$(COLOR_RESET)"
	@echo "* FLAVORED_EDX_RELEASE_PATH  : $(COLOR_INFO)$(FLAVORED_EDX_RELEASE_PATH)$(COLOR_RESET)"
	@echo "* EDX_RELEASE_REF            : $(COLOR_INFO)$(EDX_RELEASE_REF)$(COLOR_RESET)"
	@echo "* EDX_DEMO_RELEASE_REF       : $(COLOR_INFO)$(EDX_DEMO_RELEASE_REF)$(COLOR_RESET)"
	@echo ""
.PHONY: info

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

tree: \
  $(FLAVORED_EDX_RELEASE_PATH)/data/static/production/.keep \
  $(FLAVORED_EDX_RELEASE_PATH)/data/static/development/.keep \
  $(FLAVORED_EDX_RELEASE_PATH)/data/media/.keep \
  $(FLAVORED_EDX_RELEASE_PATH)/data/store/.keep \
  $(FLAVORED_EDX_RELEASE_PATH)/src/edx-demo-course/.keep \
  $(FLAVORED_EDX_RELEASE_PATH)/src/edx-platform/.keep
tree:  ## create data directories mounted as volumes
.PHONY: tree

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
.PHONY: help
