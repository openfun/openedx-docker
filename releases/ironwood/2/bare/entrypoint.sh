#!/usr/bin/env bash
#
# Development entrypoint
#

# Activate user's virtualenv
source /edx/app/edxapp/venv/bin/activate
exec "$@"
