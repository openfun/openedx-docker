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

WORKDIR /app/edx-platform

# Install Python requirements
# ... adding only targeted requirements files first to benefit from caching
ADD ./src/edx-platform/requirements/edx /app/edx-platform/requirements/edx
RUN pip install --src ../src -r requirements/edx/pre.txt
RUN pip install --src ../src -r requirements/edx/github.txt
RUN pip install --src ../src -r requirements/edx/base.txt
RUN pip install --src ../src -r requirements/edx/paver.txt
RUN pip install --src ../src -r requirements/edx/post.txt

# Install Javascript requirements
# ... adding only the package.json file first to benefit from caching
ADD ./src/edx-platform/package.json /app/edx-platform/package.json
RUN npm install

# Now add the complete project sources
ADD ./src/edx-platform /app/edx-platform

# Install the project Python packages
RUN pip install --src ../src -r requirements/edx/local.txt

# Add our custom settings
ADD ./settings/lms.env.json /app/lms.env.json
ADD ./settings/cms.env.json /app/cms.env.json
ADD ./settings/lms.auth.json /app/lms.auth.json
ADD ./settings/cms.auth.json /app/cms.auth.json
ADD ./settings/lms_production.py /app/edx-platform/lms/envs/production.py
ADD ./settings/cms_production.py /app/edx-platform/cms/envs/production.py

# Use Gunicorn in production as web server
CMD DJANGO_SETTINGS_MODULE=${SERVICE_VARIANT}.envs.production \
gunicorn --name=${SERVICE_VARIANT} --bind=0.0.0.0:8000 --max-requests=1000 ${SERVICE_VARIANT}.wsgi:application
