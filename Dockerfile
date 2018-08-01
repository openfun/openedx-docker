FROM ubuntu:16.04

# Install system dependencies
# Removing the package lists after installation is a good practice
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y build-essential curl g++ gcc gettext gfortran git git-core \
    graphviz graphviz-dev language-pack-en libffi-dev libfreetype6-dev libgeos-dev \
    libjpeg8-dev liblapack-dev libmysqlclient-dev libpng12-dev libreadline6 libxml2-dev \
    libxmlsec1-dev libxslt1-dev nodejs nodejs-legacy npm ntp pkg-config python-apt python-dev \
    python-pip software-properties-common swig tzdata && \
    rm -rf /var/lib/apt/lists/*

# Set container timezone and related timezones database and DST rules
# See https://serverfault.com/a/856593
ENV TZ 'Etc/UTC'
RUN echo $TZ > /etc/timezone && \
    rm /etc/localtime && \
    ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && \
    dpkg-reconfigure -f noninteractive tzdata

WORKDIR /edx/app/edxapp/edx-platform

# Install Python requirements
# -- edx requirements
# ... adding only targeted requirements files first to benefit from caching
COPY ./src/edx-platform/requirements/edx /edx/app/edxapp/edx-platform/requirements/edx
RUN pip install --src ../src -r requirements/edx/pre.txt && \
    pip install --src ../src -r requirements/edx/github.txt && \
    pip install --src ../src -r requirements/edx/base.txt && \
    pip install --src ../src -r requirements/edx/paver.txt && \
    pip install --src ../src -r requirements/edx/post.txt
# -- fun requirements
COPY ./requirements/features.txt /edx/app/edxapp/edx-platform/requirements/edx/features.txt
RUN pip install --src ../src -r requirements/edx/features.txt

# Install Javascript requirements
# ... adding only the package.json file first to benefit from caching
COPY ./src/edx-platform/package.json /edx/app/edxapp/edx-platform/package.json
RUN npm install

# Now add the complete project sources
COPY ./src/edx-platform /edx/app/edxapp/edx-platform

# Install the project Python packages
RUN pip install --src ../src -r requirements/edx/local.txt

# Configuration files should be mounted in "/config"
# Point to them with symbolic links
COPY ./config /config
RUN ln -sf /config/lms /edx/app/edxapp/edx-platform/lms/envs/fun && \
    ln -sf /config/cms /edx/app/edxapp/edx-platform/cms/envs/fun

# Update assets
# - Add minimal settings just to enable updating assets during container build
COPY ./config/docker_build.py /edx/app/edxapp/edx-platform/lms/envs/
COPY ./config/docker_build.py /edx/app/edxapp/edx-platform/cms/envs/
# - Update assets skipping collectstatic (it should be done during deployment)
RUN paver update_assets --settings=docker_build --skip-collect

# Use Gunicorn in production as web server
CMD DJANGO_SETTINGS_MODULE=${SERVICE_VARIANT}.envs.fun.docker_run \
    gunicorn --name=${SERVICE_VARIANT} --bind=0.0.0.0:8000 --max-requests=1000 ${SERVICE_VARIANT}.wsgi:application
