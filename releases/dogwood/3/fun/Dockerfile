# EDX-PLATFORM multi-stage docker build

ARG DOCKER_UID=1000
ARG DOCKER_GID=1000
ARG EDX_BASE_IMAGE=fundocker/edxapp:dogwood.3-fun-1.18.3
ARG EDXAPP_STATIC_ROOT=/edx/app/edxapp/staticfiles
ARG NGINX_IMAGE_NAME=fundocker/openshift-nginx
ARG NGINX_IMAGE_TAG=1.13

# === BASE ===
FROM ${EDX_BASE_IMAGE} as base

# === BUILDER ===
FROM base as builder

USER root:root

# Install builder system dependencies
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y \
      rdfind \
      ruby1.9.1-dev \
      rubygems1.9.1 && \
    rm -rf /var/lib/apt/lists/*

# Install Javascript requirements
RUN npm install

# Install Ruby dependencies
RUN gem install bundler -v 1.17.3 && \
    bundle install

# Update only fun requirements
COPY ./requirements.txt /edx/app/edxapp/edx-platform/requirements/edx/fun.txt
RUN pip install -r requirements/edx/fun.txt

# Update assets skipping collectstatic
RUN NO_PREREQ_INSTALL=1 \
    paver update_assets --settings=fun.docker_build_production --skip-collect

# === STATIC LINKS COLLECTOR ===
FROM builder as links_collector

ARG EDXAPP_STATIC_ROOT

RUN python manage.py lms collectstatic --link --noinput --settings=fun.docker_build_production && \
    python manage.py cms collectstatic --link --noinput --settings=fun.docker_build_production

# Replace duplicated file by a symlink to decrease the overall size of the
# final image
RUN rdfind -makesymlinks true -followsymlinks true ${EDXAPP_STATIC_ROOT}

# === STATIC FILES COLLECTOR ===
FROM builder as files_collector

ARG EDXAPP_STATIC_ROOT

RUN python manage.py lms collectstatic --noinput --settings=fun.docker_build_production && \
    python manage.py cms collectstatic --noinput --settings=fun.docker_build_production

# Replace duplicated file by a symlink to decrease the overall size of the
# final image
RUN rdfind -makesymlinks true ${EDXAPP_STATIC_ROOT}

# === DEVELOPMENT ===
FROM builder as development

ARG DOCKER_UID
ARG DOCKER_GID
ARG EDX_RELEASE_REF

# Install system dependencies
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y \
      git \
      libsqlite3-dev \
      mongodb && \
    rm -rf /var/lib/apt/lists/*

RUN groupadd --gid ${DOCKER_GID} edx || \
    echo "Group with ID ${DOCKER_GID} already exists." && \
    useradd \
      --create-home \
      --home-dir /home/edx \
      --uid ${DOCKER_UID} \
      --gid ${DOCKER_GID} \
      edx || \
    echo "Skip user creation (user with ID ${DOCKER_UID} already exists?)" && \
    git config --global user.name edx && \
    git config --global user.email edx@example.com

# To prevent permission issues related to the non-priviledged user running in
# development, we will install development dependencies in a python virtual
# environment belonging to that user
RUN pip install virtualenv==16.7.9

# Create the virtualenv directory where we will install python development
# dependencies
RUN mkdir -p /edx/app/edxapp/venv && \
    chown -R ${DOCKER_UID}:${DOCKER_GID} /edx/app/edxapp/venv

# Change edxapp directory owner to allow the development image docker user to
# perform installations from edxapp sources (yeah, I know...)
RUN chown -R ${DOCKER_UID}:${DOCKER_GID} /edx/app/edxapp

# Copy the entrypoint that will activate the virtualenv
COPY ./entrypoint.sh /usr/local/bin/entrypoint.sh

# Change sass-cache owner so that the development user has write permission.
# This is required to run the update_assets paver task in development.
RUN chown -R ${DOCKER_UID}:${DOCKER_GID} /tmp/sass-cache

# Switch to an un-privileged user matching the host user to prevent permission
# issues with volumes (host folders)
USER ${DOCKER_UID}:${DOCKER_GID}

# Create the virtualenv with a non-priviledged user
RUN virtualenv -p python2.7 --system-site-packages /edx/app/edxapp/venv

# Install development dependencies in a virtualenv (we need to downgrade pip
# for that)
RUN bash -c "source /edx/app/edxapp/venv/bin/activate && \
    pip install --upgrade pip==9.0.3 && \
    pip install --no-cache-dir -r requirements/edx/development.txt"

# Re-upgrade pip in the virtualenv for further install (when using sources with
# volumes)
RUN bash -c "source /edx/app/edxapp/venv/bin/activate && \
    pip install --upgrade pip"

ENTRYPOINT [ "/usr/local/bin/entrypoint.sh" ]

# === PRODUCTION ===
FROM base as production

ARG EDXAPP_STATIC_ROOT

USER root:root

# Apply security updates
RUN apt-get update && \
    apt-get upgrade -y && \
    rm -rf /var/lib/apt/lists/*

# Copy static files
COPY --from=links_collector ${EDXAPP_STATIC_ROOT} ${EDXAPP_STATIC_ROOT}

# Now that dependencies are installed and configuration has been set, the above
# statements will run with a un-privileged user.
USER 10000

# === NGINX ===
FROM ${NGINX_IMAGE_NAME}:${NGINX_IMAGE_TAG} as nginx

ARG EDXAPP_STATIC_ROOT

RUN mkdir -p ${EDXAPP_STATIC_ROOT}

COPY --from=files_collector ${EDXAPP_STATIC_ROOT} ${EDXAPP_STATIC_ROOT}
