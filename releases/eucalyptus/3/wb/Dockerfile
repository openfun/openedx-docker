# EDX-PLATFORM multi-stage docker build

# Change release to build, by providing the EDX_RELEASE_REF build argument to
# your build command:
#
# $ docker build \
#     --build-arg EDX_RELEASE_REF="open-release/eucalyptus.3" \
#     -t edxapp:eucalyptus.3 \
#     .
ARG DOCKER_UID=1000
ARG DOCKER_GID=1000
ARG EDX_RELEASE_REF=fun/whitebrand
ARG EDX_ARCHIVE_URL=https://github.com/openfun/edx-platform/archive/fun/whitebrand.tar.gz

# === BASE ===
FROM ubuntu:16.04 as base

# Configure locales and timezone
RUN apt-get update && \
    apt-get install -y \
      gettext \
      libreadline6 \
      locales \
      tzdata && \
    rm -rf /var/lib/apt/lists/*
RUN sed -i 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen && \
    locale-gen
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8


# === DOWNLOAD ===
FROM base as downloads

WORKDIR /downloads

# Install curl
RUN apt-get update && \
    apt-get install -y curl

# Download pip installer
RUN curl -sLo get-pip.py https://bootstrap.pypa.io/get-pip.py

# Download edxapp release
# Get default EDX_RELEASE_REF value (defined on top)
ARG EDX_RELEASE_REF
ARG EDX_ARCHIVE_URL
RUN curl -sLo edxapp.tgz $EDX_ARCHIVE_URL && \
    tar xzf edxapp.tgz


# === EDXAPP ===
FROM base as edxapp

# Install base system dependencies
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y python && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /edx/app/edxapp/edx-platform

# Get default EDX_RELEASE_REF value (defined on top)
ARG EDX_RELEASE_REF
COPY --from=downloads /downloads/edx-platform-* .

COPY ./requirements.txt /edx/app/edxapp/edx-platform/requirements/edx/fun.txt

# We copy default configuration files to "/config" and we point to them via
# symlinks. That allows to easily override default configurations by mounting a
# docker volume.
COPY ./config /config
RUN ln -sf /config/lms /edx/app/edxapp/edx-platform/lms/envs/fun && \
    ln -sf /config/cms /edx/app/edxapp/edx-platform/cms/envs/fun

# Add node_modules/.bin to the PATH so that paver-related commands can execute
# node scripts
ENV PATH="/edx/app/edxapp/edx-platform/node_modules/.bin:${PATH}"

# === BUILDER ===
FROM edxapp as builder

WORKDIR /builder

# Install builder system dependencies
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y \
      build-essential \
      gettext \
      git \
      graphviz-dev \
      libgeos-dev \
      libjpeg8-dev \
      libmysqlclient-dev \
      libpng12-dev \
      libxml2-dev \
      libxmlsec1-dev \
      nodejs \
      nodejs-legacy \
      npm \
      python-dev && \
    rm -rf /var/lib/apt/lists/*

# Install the latest pip release
COPY --from=downloads /downloads/get-pip.py ./get-pip.py
RUN python get-pip.py

WORKDIR /edx/app/edxapp/edx-platform

# Install python dependencies
#
# Note that we force some pinned release installations before installing github
# dependencies to prevent secondary dependencies installation to fail while
# trying to install a python 2.7 incompatible release
RUN pip install -r requirements/edx/pre.txt
RUN pip install \
      astroid==1.6.0 \
      django==1.8.15 \
      pip==9.0.3
RUN pip install --src /usr/local/src -r requirements/edx/github.txt
RUN pip install -r requirements/edx/base.txt
RUN pip install -r requirements/edx/paver.txt
RUN pip install -r requirements/edx/post.txt
RUN pip install -r requirements/edx/local.txt
# Redis is an extra requirement of Celery, we need to install it explicitly so
# that celery workers are effective
RUN pip install redis==3.3.7
# Installing FUN requirements needs a recent pip release (we are using
# setup.cfg declarative packages)
RUN pip install -r requirements/edx/fun.txt

# Install Javascript requirements
RUN npm install

# Force the reinstallation of edx-ui-toolkit's dependencies inside its
# node_modules because someone is poking files from there when updating assets.
RUN cd node_modules/edx-ui-toolkit && \
      npm install

# Update assets skipping collectstatic (it should be done during deployment)
RUN NO_PREREQ_INSTALL=1 \
    paver update_assets --settings=fun.docker_build_production --skip-collect


# === DEVELOPMENT ===
FROM builder as development

ARG DOCKER_UID
ARG DOCKER_GID
ARG EDX_RELEASE_REF

# Install system dependencies
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y \
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
      edx

# To prevent permission issues related to the non-priviledged user running in
# development, we will install development dependencies in a python virtual
# environment belonging to that user
RUN pip install virtualenv

# Create the virtualenv directory where we will install python development
# dependencies
RUN mkdir -p /edx/app/edxapp/venv && \
    chown -R ${DOCKER_UID}:${DOCKER_GID} /edx/app/edxapp/venv

# Change edxapp directory owner to allow the development image docker user to
# perform installations from edxapp sources (yeah, I know...)
RUN chown -R ${DOCKER_UID}:${DOCKER_GID} /edx/app/edxapp

# Copy the entrypoint that will activate the virtualenv
COPY ./entrypoint.sh /usr/local/bin/entrypoint.sh

# Switch to an un-privileged user matching the host user to prevent permission
# issues with volumes (host folders)
USER ${DOCKER_UID}:${DOCKER_GID}

# Create the virtualenv with a non-priviledged user
RUN virtualenv -p python2.7 --system-site-packages /edx/app/edxapp/venv

# Install development dependencies in a virtualenv
RUN bash -c "source /edx/app/edxapp/venv/bin/activate && \
      pip install --no-cache-dir -r requirements/edx/local.txt && \
      pip install --no-cache-dir -r requirements/edx/development.txt"

ENTRYPOINT [ "/usr/local/bin/entrypoint.sh" ]


# === PRODUCTION ===
FROM edxapp as production

# Install runner system dependencies
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y \
      libgeos-dev \
      libjpeg8 \
      libmysqlclient20 \
      libpng12-0 \
      libxml2 \
      libxmlsec1-dev \
      lynx \
      nodejs \
      nodejs-legacy \
      tzdata && \
    rm -rf /var/lib/apt/lists/*

# Copy installed dependencies
COPY --from=builder /usr/local /usr/local

# Copy modified sources (sic!)
COPY --from=builder /edx/app/edxapp/edx-platform  /edx/app/edxapp/edx-platform

# Now that dependencies are installed and configuration has been set, the above
# statements will run with a un-privileged user.
USER 10000

# To start the CMS, inject the SERVICE_VARIANT=cms environment variable
# (defaults to "lms")
ENV SERVICE_VARIANT=lms

# Use Gunicorn in production as web server
CMD DJANGO_SETTINGS_MODULE=${SERVICE_VARIANT}.envs.fun.docker_run \
    gunicorn --name=${SERVICE_VARIANT} --bind=0.0.0.0:8000 --max-requests=1000 ${SERVICE_VARIANT}.wsgi:application
