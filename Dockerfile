# EDX-PLATFORM multi-stage docker build

# Change release to build, by providing the EDXAPP_RELEASE_ARCHIVE_URL build argument to
# your build command:
#
# $ docker build \
#     --build-arg EDXAPP_RELEASE_ARCHIVE_URL="https://github.com/edx/edx-platform/archive/master.tar.gz" \
#     -t edxapp:latest \
#     .
ARG EDXAPP_RELEASE_ARCHIVE_URL=https://github.com/edx/edx-platform/archive/master.tar.gz

# === BASE ===
FROM ubuntu:16.04 as base

# Configure locales
RUN apt-get update && \
    apt-get install -y gettext locales && \
    rm -rf /var/lib/apt/lists/*
RUN sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen && \
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

# Download edxapp release
# Get default EDXAPP_RELEASE_ARCHIVE_URL value (defined on top)
ARG EDXAPP_RELEASE_ARCHIVE_URL
RUN curl -sLo edxapp.tgz $EDXAPP_RELEASE_ARCHIVE_URL && \
    tar xzf edxapp.tgz


# === EDXAPP ===
FROM base as edxapp

# Install base system dependencies
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y python && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /edx/app/edxapp/edx-platform

# Get default EDXAPP_RELEASE_ARCHIVE_URL value (defined on top)
ARG EDXAPP_RELEASE_ARCHIVE_URL
COPY --from=downloads /downloads/edx-platform-* .

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
    coffeescript \
    curl \
    g++ \
    gcc \
    gettext \
    gfortran \
    git \
    git-core \
    graphviz \
    graphviz-dev \
    language-pack-en \
    libatlas-dev \
    libblas-dev \
    libffi-dev \
    libfreetype6-dev \
    libgeos-dev \
    libgeos-ruby1.8 \
    libgraphviz-dev \
    libjpeg-dev \
    libjpeg8-dev \
    liblapack-dev \
    libmysqlclient-dev \
    libpng12-dev \
    libreadline6 \
    libreadline6-dev \
    libxml2-dev \
    libxmlsec1-dev \
    libxslt-dev \
    libxslt1-dev \
    locales \
    lynx-cur \
    mysql-client \
    nodejs \
    npm \
    ntp \
    pkg-config \
    python-apt \
    python-scipy \
    python-dev \
    python-numpy \
    python-pip \
    python-software-properties \
    software-properties-common \
    swig \
    yui-compressor \
    zlib1g-dev \
    wget libssl-dev && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /edx/app/edxapp/edx-platform

# Install python dependencies
RUN pip -V
RUN pip install --src /usr/local/src -r requirements/edx/pre.txt && \
    pip install --src /usr/local/src -r requirements/edx/github.txt && \
    pip install --src /usr/local/src -r requirements/edx/base.txt && \
    pip install --src /usr/local/src -r requirements/edx/paver.txt && \
    pip install --src /usr/local/src -r requirements/edx/post.txt && \
    pip install --src /usr/local/src -r requirements/edx/local.txt

# Install Javascript requirements
RUN ln -s /usr/bin/nodejs /usr/bin/node
RUN npm install

# Force the reinstallation of edx-ui-toolkit's dependencies inside its node_modules
# because someone is poking files from there when updating assets.
RUN cd /edx/app/edxapp/edx-platform/node_modules/edx-ui-toolkit && npm install

# Update assets skipping collectstatic (it should be done during deployment)
RUN NO_PREREQ_INSTALL=1 \
    paver update_assets --settings=fun.docker_build_production --skip-collect


# === DEVELOPMENT ===
FROM builder as development

ARG UID=1000
ARG GID=1000
ARG EDXAPP_RELEASE_ARCHIVE_URL

# Install system dependencies
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y \
    dnsutils \
    iputils-ping \
    libsqlite3-dev \
    mongodb \
    vim && \
    rm -rf /var/lib/apt/lists/*

# To prevent permission issues related to the non-priviledged user running in
# development, we will install development dependencies in a python virtual
# environment belonging to that user
RUN pip install virtualenv

# Create the virtualenv directory where we will install python development
# dependencies
RUN mkdir -p /edx/app/edxapp/venv && \
    chown -R ${UID}:${GID} /edx/app/edxapp/venv

# Change edxapp directory owner to allow the development image docker user to
# perform installations from edxapp sources (yeah, I know...)
RUN chown -R ${UID}:${GID} /edx/app/edxapp

# Copy the entrypoint that will activate the virtualenv
COPY ./docker/files/usr/local/bin/entrypoint.sh /usr/local/bin/entrypoint.sh

# Switch to an un-privileged user matching the host user to prevent permission
# issues with volumes (host folders)
USER ${UID}:${GID}

# Create the virtualenv with a non-priviledged user
RUN virtualenv -p python2.7 --system-site-packages /edx/app/edxapp/venv

# Install development dependencies in a virtualenv
RUN bash -c "source /edx/app/edxapp/venv/bin/activate && \
    pip install --no-cache-dir -r requirements/edx/development.txt"

ENTRYPOINT [ "/usr/local/bin/entrypoint.sh" ]


# === PRODUCTION ===
FROM edxapp as production

# Install runner system dependencies
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y \
    libgeos-dev \
    libmysqlclient20 \
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

# Set container timezone and related timezones database and DST rules
# See https://serverfault.com/a/856593
ENV TZ 'Etc/UTC'
RUN echo $TZ > /etc/timezone && \
    rm /etc/localtime && \
    ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && \
    dpkg-reconfigure -f noninteractive tzdata

# Now that dependencies are installed and configuration has been set, the above
# statements will run with a un-privileged user.
USER 10000

# To start the CMS, inject the SERVICE_VARIANT=cms environment variable
# (defaults to "lms")
ENV SERVICE_VARIANT=lms

# Use Gunicorn in production as web server
CMD DJANGO_SETTINGS_MODULE=${SERVICE_VARIANT}.envs.fun.docker_run \
    gunicorn --name=${SERVICE_VARIANT} --bind=0.0.0.0:8000 --max-requests=1000 ${SERVICE_VARIANT}.wsgi:application
