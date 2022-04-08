#!/usr/bin/env bash
#
# Development entrypoint
#

# Activate user's virtualenv
source /edx/app/edxapp/venv/bin/activate

# Override default root_urls for the lms app
ln -sf /config/lms/root_urls.py /edx/app/edxapp/edx-platform/lms/

exec "$@"
