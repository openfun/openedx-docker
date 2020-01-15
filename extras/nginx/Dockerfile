# OpenEdx Docker extra: NGINX
#
# This image will bundle all static files from an openedx-docker release in the
# /data/static directory.
#
# Usage:
#
#   docker build \
#     --build-arg EDXAPP_IMAGE_TAG=dogwood.3-1.2.1 \
#     -t edxapp-nginx:latest \
#     .
#
ARG EDXAPP_IMAGE_NAME=fundocker/edxapp
ARG EDXAPP_IMAGE_TAG
ARG EDXAPP_STATIC_ROOT=/edx/app/edxapp/staticfiles
ARG NGINX_IMAGE_NAME=fundocker/openshift-nginx
ARG NGINX_IMAGE_TAG=1.13

# === EDXAPP ===
FROM ${EDXAPP_IMAGE_NAME}:${EDXAPP_IMAGE_TAG} as edxapp

ARG EDXAPP_STATIC_ROOT

USER root:root

RUN apt-get update && \
    apt-get install -y rdfind && \
    rm -rf /var/lib/apt/lists/*

RUN python manage.py lms collectstatic --noinput --settings=fun.docker_run && \
    python manage.py cms collectstatic --noinput --settings=fun.docker_run

# Replace duplicated file by a symlink to decrease the overall size of the
# final image
RUN rdfind -makesymlinks true /edx/app/edxapp/staticfiles

# === NGINX (final image) ===
FROM ${NGINX_IMAGE_NAME}:${NGINX_IMAGE_TAG}

ARG EDXAPP_STATIC_ROOT

RUN mkdir -p ${EDXAPP_STATIC_ROOT}

COPY --from=edxapp ${EDXAPP_STATIC_ROOT} ${EDXAPP_STATIC_ROOT}
