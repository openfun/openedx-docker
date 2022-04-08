# EDX-PLATFORM multi-stage docker build

# Change release to build, by providing the EDX_RELEASE_REF build argument to
# your build command:
#
# $ docker build \
#     --build-arg EDX_RELEASE_REF="named-release/dogwood.3" \
#     -t edxapp:dogwood.3-fun \
#     .
ARG DOCKER_UID=1000
ARG DOCKER_GID=1000
ARG EDX_RELEASE_REF=dogwood.3-fun-5.3.3
ARG EDX_ARCHIVE_URL=https://github.com/openfun/edx-platform/archive/dogwood.3-fun-5.3.3.tar.gz
ARG EDXAPP_STATIC_ROOT=/edx/app/edxapp/staticfiles
ARG NGINX_IMAGE_NAME=nginxinc/nginx-unprivileged
ARG NGINX_IMAGE_TAG=1.20
ARG PYTHON_VERSION=2.7.18


# === BASE ===
FROM ubuntu:12.04 as base

# System dependencies
RUN sed -i.bak -r 's/(archive|security).ubuntu.com/old-releases.ubuntu.com/g' /etc/apt/sources.list && \
    apt-get update && \
    apt-get install -y \
      gcc \
      gettext \
      libssl-dev \
      locales \
      make \
      tzdata \
      zlib1g-dev && \
    rm -rf /var/lib/apt/lists/*

# Configure locales and timezone
RUN echo 'en_US.UTF-8 UTF-8' > /var/lib/locales/supported.d/local && \
    dpkg-reconfigure locales
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

# Upgrade Python 2.7 to its latest version from source
WORKDIR /tmp/

ARG PYTHON_VERSION
RUN curl -sLo Python-${PYTHON_VERSION}.tgz https://www.python.org/ftp/python/${PYTHON_VERSION}/Python-${PYTHON_VERSION}.tgz \
  && tar --extract -f Python-${PYTHON_VERSION}.tgz \
  && cd ./Python-${PYTHON_VERSION}/ \
  && ./configure --enable-optimizations --prefix=/usr/local \
  && make && make install \
  && cd ../ \
  && rm -r ./Python-${PYTHON_VERSION}*


# === DOWNLOAD ===
FROM base as downloads

WORKDIR /downloads

# Download pip installer for python 2.7
RUN curl -sLo get-pip.py https://bootstrap.pypa.io/pip/2.7/get-pip.py

# Download edxapp release
ARG EDX_ARCHIVE_URL
RUN curl -sLo edxapp.tgz $EDX_ARCHIVE_URL && \
    tar xzf edxapp.tgz


# === EDXAPP ===
FROM base as edxapp

# Install apt https support (required to use node sources repository)
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y \
      apt-transport-https

# Add a recent release of nodejs to apt sources (ubuntu package for precise is
# broken)
RUN echo "deb https://deb.nodesource.com/node_10.x trusty main" \
	> /etc/apt/sources.list.d/nodesource.list && \
    curl -s 'https://deb.nodesource.com/gpgkey/nodesource.gpg.key' | apt-key add -

# Install base system dependencies
RUN apt-get update && \
    apt-get install -y \
      nodejs && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /edx/app/edxapp/edx-platform

COPY --from=downloads /downloads/edx-platform-* .

COPY ./requirements.txt /edx/app/edxapp/edx-platform/requirements/edx/fun.txt

# We copy default configuration files to "/config" and we point to them via
# symlinks. That allows to easily override default configurations by mounting a
# docker volume.
COPY ./config /config
RUN ln -sf /config/lms /edx/app/edxapp/edx-platform/lms/envs/fun && \
    ln -sf /config/cms /edx/app/edxapp/edx-platform/cms/envs/fun && \
    ln -sf /config/lms/root_urls.py /edx/app/edxapp/edx-platform/lms/
# Add node_modules/.bin to the PATH so that paver-related commands can execute
# node scripts
ENV PATH="/edx/app/edxapp/edx-platform/node_modules/.bin:${PATH}"

# OpenEdx requires this environment variable to be defined, or else, it will
# try to get the current Git reference. Since we don't use a Git clone to
# build this release, we force the revision to be the release reference.
ARG EDX_RELEASE_REF
ENV EDX_PLATFORM_REVISION=${EDX_RELEASE_REF:-named-release/dogwood.3}


# === BUILDER ===
FROM edxapp as builder

WORKDIR /builder

# Install builder system dependencies
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y \
      build-essential \
      gfortran \
      git-core \
      graphviz \
      graphviz-dev \
      language-pack-en \
      libffi-dev \
      libfreetype6-dev \
      libgeos-dev \
      libjpeg8-dev \
      liblapack-dev \
      libmysqlclient-dev \
      libxml2-dev \
      libxmlsec1-dev \
      libxslt1-dev \
      pkg-config \
      rdfind \
      ruby1.9.1-dev \
      software-properties-common \
      swig && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /edx/app/edxapp/edx-platform

# Install Javascript requirements
RUN npm install

# Install Ruby dependencies
RUN gem install bundler -v 1.17.3 && \
    bundle install

COPY --from=downloads /downloads/get-pip.py ./get-pip.py
RUN python get-pip.py

# Install python dependencies
#
RUN pip install -r requirements/edx/pre.txt
# We need specific versions of pip and setuptools to handle the different
# ways to declare Python dependencies in OpenEdX 😅
# Voluptuous is a sub-dependency. The version match pattern is >=0.10.5,<1.0.0
# but the version 0.13.0 is incompatible with this version of OpenEdX so we install
# manually the latest compatible version to prevent the installation of 0.13.0
RUN pip install \
    pip==9.0.3 \
    setuptools==44.1.1 \
    voluptuous==0.12.2

RUN pip install --src /usr/local/src -r requirements/edx/github.txt
# Uninstall django==1.4.22 which gets installed because of django-wiki.
# Otherwise 1.8.12 is installed on top of 1.4.22 in the next step and causes
# a build failure.
RUN pip uninstall --yes django
RUN pip install -r requirements/edx/base.txt
RUN pip install -r requirements/edx/paver.txt
RUN pip install -r requirements/edx/post.txt
# Upgrade pip once again so that eggs (local.txt) are properly installed
RUN pip install --upgrade pip
RUN pip install -r requirements/edx/local.txt
# Installing FUN requirements needs a recent pip release (we are using
# setup.cfg declarative packages)
RUN pip install -r requirements/edx/fun.txt

# Update assets skipping collectstatic (it should be done during deployment)
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

# To prevent permission issues related to the non-privileged user running in
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

# Create the virtualenv with a non-privileged user
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
FROM edxapp as production

ARG EDXAPP_STATIC_ROOT

# Install runner system dependencies
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y \
    libgeos-dev \
    libjpeg8 \
    libmysqlclient18 \
    libxml2 \
    libxmlsec1-dev \
    lynx \
    tzdata && \
    rm -rf /var/lib/apt/lists/*

# Copy installed dependencies
COPY --from=builder /usr/local /usr/local

# Copy modified sources (sic!)
COPY --from=builder /edx/app/edxapp/edx-platform  /edx/app/edxapp/edx-platform

# Copy static files
COPY --from=links_collector ${EDXAPP_STATIC_ROOT} ${EDXAPP_STATIC_ROOT}

# Now that dependencies are installed and configuration has been set, the above
# statements will run with a un-privileged user.
USER 10000

# To start the CMS, inject the SERVICE_VARIANT=cms environment variable
# (defaults to "lms")
ENV SERVICE_VARIANT=lms

# Gunicorn configuration
#
# As some synchronous requests may be quite long (e.g. courses import), we
# should make timeout rather high and configurable so that it could be
# increased without having to make a new release of this image
#
ENV GUNICORN_TIMEOUT 300

# In docker we must increase the number of workers and threads created
# by gunicorn.
# This blogpost explains why and how to do that https://pythonspeed.com/articles/gunicorn-in-docker/
ENV GUNICORN_WORKERS 3
ENV GUNICORN_THREADS 6

# Use Gunicorn in production as web server
CMD DJANGO_SETTINGS_MODULE=${SERVICE_VARIANT}.envs.fun.docker_run \
    gunicorn \
      --name=${SERVICE_VARIANT} \
      --bind=0.0.0.0:8000 \
      --max-requests=1000 \
      --timeout=${GUNICORN_TIMEOUT} \
      --workers=${GUNICORN_WORKERS} \
      --threads=${GUNICORN_THREADS} \
      ${SERVICE_VARIANT}.wsgi:application


# === NGINX ===
FROM ${NGINX_IMAGE_NAME}:${NGINX_IMAGE_TAG} as nginx

ARG EDXAPP_STATIC_ROOT

# Switch back to the root user to include static files in the container
USER root:root

RUN mkdir -p ${EDXAPP_STATIC_ROOT}

COPY --from=files_collector ${EDXAPP_STATIC_ROOT} ${EDXAPP_STATIC_ROOT}

# Now that everything is included, run the container with a un-privileged user
USER 10000
