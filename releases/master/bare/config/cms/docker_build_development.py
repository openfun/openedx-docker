# This is a minimal settings file allowing us to run "update_assets"
# in the Dockerfile for the development image of the edxapp CMS

from .docker_build_production import *

DEBUG = True
REQUIRE_DEBUG = True

WEBPACK_CONFIG_PATH = "webpack.dev.config.js"
