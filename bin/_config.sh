#!/usr/bin/env bash

PROJECT_DIRECTORY=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/..
RELEASES_DIRECTORY="releases"
NGINX_CONF_DIRECTORY="docker/files/etc/nginx/conf.d"

export PROJECT_DIRECTORY
export RELEASES_DIRECTORY
