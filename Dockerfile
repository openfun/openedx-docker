FROM ubuntu:16.04

# Install system dependencies
# Removing the package lists after installation is a good practice
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y build-essential curl g++ gcc gettext gfortran git git-core \
    graphviz graphviz-dev language-pack-en libffi-dev libfreetype6-dev libgeos-dev \
    libjpeg8-dev liblapack-dev libmysqlclient-dev libpng12-dev libxml2-dev \
    libxmlsec1-dev libxslt1-dev nodejs nodejs-legacy npm ntp pkg-config python-apt python-dev \
    python-pip software-properties-common swig && \
    rm -rf /var/lib/apt/lists/*

# Note: we should do things in order of "least chance to change" but
# it is not possible because the python requirements are installing
# repositories within the project source code!

# Add the complete project source
WORKDIR /app/edx-platform
ADD ./src/edx-platform /app/edx-platform
ADD ./settings/lms.env.json /app/lms.env.json
ADD ./settings/cms.env.json /app/cms.env.json
ADD ./settings/lms.auth.json /app/lms.auth.json
ADD ./settings/cms.auth.json /app/cms.auth.json
ADD ./settings/lms_production.py /app/edx-platform/lms/envs/production.py
ADD ./settings/cms_production.py /app/edx-platform/cms/envs/production.py

# Install Python requirements
RUN pip install --src ../src -r requirements/edx/pre.txt
RUN pip install --src ../src -r requirements/edx/github.txt
RUN pip install --src ../src -r requirements/edx/local.txt
RUN pip install --src ../src -r requirements/edx/base.txt
RUN pip install --src ../src -r requirements/edx/paver.txt
RUN pip install --src ../src -r requirements/edx/post.txt

# Install Javascript requirements
RUN npm install

# Use Gunicorn in production as web server
CMD DJANGO_SETTINGS_MODULE=${SERVICE_VARIANT}.envs.production \
gunicorn --name=${SERVICE_VARIANT} --bind=0.0.0.0:8000 --max-requests=1000 ${SERVICE_VARIANT}.wsgi:application

