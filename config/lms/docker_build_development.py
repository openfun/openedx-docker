# This is a minimal settings file allowing us to run "update_assets"
# in the Dockerfile for the development image of the edxapp LMS

from .docker_build_production import *

DEBUG = True
WEBPACK_CONFIG_PATH = "webpack.dev.config.js"
