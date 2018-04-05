FROM ubuntu:16.04

# Install system dependencies
# Removing the package lists after installation is a good practice
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y build-essential curl g++ gcc gettext gfortran git git-core \
    graphviz graphviz-dev language-pack-en libffi-dev libfreetype6-dev libgeos-dev \
    libjpeg8-dev liblapack-dev libmysqlclient-dev libpng12-dev libxml2-dev \
    libxmlsec1-dev libxslt1-dev nodejs nodejs-legacy npm ntp pkg-config python-apt python-dev \
    python-pip ruby software-properties-common swig tzdata && \
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
# ... adding only targeted requirements files first to benefit from caching
ADD ./src/edx-platform/requirements/edx /edx/app/edxapp/edx-platform/requirements/edx
RUN pip install --src ../src -r requirements/edx/pre.txt && \
    pip install --src ../src -r requirements/edx/github.txt && \
    pip install --src ../src -r requirements/edx/base.txt && \
    pip install --src ../src -r requirements/edx/paver.txt && \
    pip install --src ../src -r requirements/edx/post.txt

# Install Javascript requirements
# ... adding only the package.json file first to benefit from caching
ADD ./src/edx-platform/package.json /edx/app/edxapp/edx-platform/package.json
RUN npm install

# Now add the complete project sources
ADD ./src/edx-platform /edx/app/edxapp/edx-platform
RUN mkdir -p /edx/app/edxapp/edx-platform/lms/envs/fun && \
    mkdir -p /edx/app/edxapp/edx-platform/cms/envs/fun

# Dogwood assets building requires a Ruby stack
RUN gem install bundle
RUN bundle install

# Install the project Python packages
RUN pip install --src ../src -r requirements/edx/local.txt

# Add /config dir to container and link settings files
ADD /config /config

RUN ln -sf /config/docker_run_lms_production.py /edx/app/edxapp/edx-platform/lms/envs/fun/docker_run_production.py && \
    ln -sf /config/docker_run_lms_preprod.py /edx/app/edxapp/edx-platform/lms/envs/fun/docker_run_preprod.py && \
    ln -sf /config/docker_run_lms_staging.py /edx/app/edxapp/edx-platform/lms/envs/fun/docker_run_staging.py && \
    ln -sf /config/docker_run_lms_dev.py /edx/app/edxapp/edx-platform/lms/envs/fun/docker_run_dev.py && \
    ln -sf /config/docker_run_lms_test.py /edx/app/edxapp/edx-platform/lms/envs/fun/docker_run_test.py && \
    ln -sf /config/shared_settings.py /edx/app/edxapp/edx-platform/lms/envs/fun/shared_settings.py && \
    ln -sf /config/shared_test.py /edx/app/edxapp/edx-platform/lms/envs/fun/shared_test.py && \
    ln -sf /config/utils.py /edx/app/edxapp/edx-platform/lms/envs/fun/utils.py && \
    touch /edx/app/edxapp/edx-platform/lms/envs/fun/__init__.py && \
    ln -sf /config/docker_run_cms_production.py /edx/app/edxapp/edx-platform/cms/envs/fun/docker_run_production.py && \
    ln -sf /config/docker_run_cms_preprod.py /edx/app/edxapp/edx-platform/cms/envs/fun/docker_run_preprod.py && \
    ln -sf /config/docker_run_cms_staging.py /edx/app/edxapp/edx-platform/cms/envs/fun/docker_run_staging.py && \
    ln -sf /config/docker_run_cms_dev.py /edx/app/edxapp/edx-platform/cms/envs/fun/docker_run_dev.py && \
    ln -sf /config/docker_run_cms_test.py /edx/app/edxapp/edx-platform/cms/envs/fun/docker_run_test.py && \
    ln -sf /config/shared_settings.py /edx/app/edxapp/edx-platform/cms/envs/fun/shared_settings.py && \
    ln -sf /config/shared_test.py /edx/app/edxapp/edx-platform/cms/envs/fun/shared_test.py && \
    ln -sf /config/utils.py /edx/app/edxapp/edx-platform/cms/envs/fun/utils.py && \
    touch /edx/app/edxapp/edx-platform/cms/envs/fun/__init__.py

# Update assets
# - Add minimal settings just to enable updating assets during container build
ADD ./config/docker_build.py /edx/app/edxapp/edx-platform/lms/envs/
ADD ./config/docker_build.py /edx/app/edxapp/edx-platform/cms/envs/
# - Update assets skipping collectstatic (it should be done during deployment)
RUN paver update_assets --settings=docker_build --skip-collect

# fun-apps requirements

ADD ./src/fun-apps/requirements /edx/app/edxapp/fun-apps/requirements
RUN pip install --src ../src  -r ../fun-apps/requirements/base.txt
RUN pip install --src ../src  -r ../fun-apps/requirements/ipython-xblock.txt


ADD ./src/fun-apps /edx/app/edxapp/fun-apps

RUN mkdir -p /edx/app/edxapp/data && \
    mkdir -p /edx/var/edxapp/attestations && \
    mkdir -p /edx/var/edxapp/shared/openassessment_submissions && \
    mkdir -p /edx/var/edxapp/shared/openassessment_submissions_cache && \
    mkdir -p /edx/var/edxapp/shared/video_subtitles_cache && \
    mkdir -p /edx/var/edxapp/shared/openassessment_submissions_cache

# Use Gunicorn in production as web server
CMD DJANGO_SETTINGS_MODULE=${SERVICE_VARIANT}.envs.fun.docker_run_production \
    gunicorn --name=${SERVICE_VARIANT} --bind=0.0.0.0:8000 --max-requests=1000 ${SERVICE_VARIANT}.wsgi:application
