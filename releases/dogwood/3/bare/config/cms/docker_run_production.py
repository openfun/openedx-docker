"""
This is the default template for our main set of AWS servers.
"""

# We intentionally define lots of variables that aren't used, and
# pylint: disable=wildcard-import, unused-wildcard-import

# Pylint gets confused by path.py instances, which report themselves as class
# objects. As a result, pylint applies the wrong regex in validating names,
# and throws spurious errors. Therefore, we disable invalid-name checking.
# pylint: disable=invalid-name

import json
import os
import platform

from lms.envs.fun.utils import Configuration
from openedx.core.lib.logsettings import get_logger_config
from path import Path as path
from xmodule.modulestore.modulestore_settings import (
    convert_module_store_setting_if_needed,
    update_module_store_settings,
)

from ..common import *


# Load custom configuration parameters from yaml files
config = Configuration(os.path.dirname(__file__))

# edX has now started using "settings.ENV_TOKENS" and "settings.AUTH_TOKENS" everywhere in the
# project, not just in the settings. Let's make sure our settings still work in this case
ENV_TOKENS = config
AUTH_TOKENS = config

# SERVICE_VARIANT specifies name of the variant used, which decides what JSON
# configuration files are read during startup.
SERVICE_VARIANT = config("SERVICE_VARIANT", default=None)

# CONFIG_ROOT specifies the directory where the JSON configuration
# files are expected to be found. If not specified, use the project
# directory.
CONFIG_ROOT = path(config("CONFIG_ROOT", default=ENV_ROOT))

# CONFIG_PREFIX specifies the prefix of the JSON configuration files,
# based on the service variant. If no variant is use, don't use a
# prefix.
CONFIG_PREFIX = SERVICE_VARIANT + "." if SERVICE_VARIANT else ""


############### ALWAYS THE SAME ################################

RELEASE = config("RELEASE", default=None)
DEBUG = False

# IMPORTANT: With this enabled, the server must always be behind a proxy that
# strips the header HTTP_X_FORWARDED_PROTO from client requests. Otherwise,
# a user can fool our server into thinking it was an https connection.
# See
# https://docs.djangoproject.com/en/dev/ref/settings/#secure-proxy-ssl-header
# for other warnings.
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

###################################### CELERY  ################################

CELERY_ALWAYS_EAGER = config("CELERY_ALWAYS_EAGER", default=False, formatter=bool)

# Don't use a connection pool, since connections are dropped by ELB.
BROKER_POOL_LIMIT = 0
BROKER_CONNECTION_TIMEOUT = 1

# For the Result Store, use the django cache named 'celery'
CELERY_RESULT_BACKEND = config(
    "CELERY_RESULT_BACKEND", default="djcelery.backends.cache:CacheBackend"
)

# When the broker is behind an ELB, use a heartbeat to refresh the
# connection and to detect if it has been dropped.
BROKER_HEARTBEAT = 60.0
BROKER_HEARTBEAT_CHECKRATE = 2

# Each worker should only fetch one message at a time
CELERYD_PREFETCH_MULTIPLIER = 1

CELERY_DEFAULT_EXCHANGE = "edx.cms.core"

# Celery queues
DEFAULT_PRIORITY_QUEUE = config(
    "DEFAULT_PRIORITY_QUEUE", default="edx.cms.core.default"
)
HIGH_PRIORITY_QUEUE = config("HIGH_PRIORITY_QUEUE", default="edx.cms.core.high")
LOW_PRIORITY_QUEUE = config("LOW_PRIORITY_QUEUE", default="edx.cms.core.low")

CELERY_DEFAULT_QUEUE = DEFAULT_PRIORITY_QUEUE
CELERY_DEFAULT_ROUTING_KEY = DEFAULT_PRIORITY_QUEUE

CELERY_QUEUES = config(
    "CELERY_QUEUES",
    default={
        DEFAULT_PRIORITY_QUEUE: {},
        HIGH_PRIORITY_QUEUE: {},
        LOW_PRIORITY_QUEUE: {},
    },
    formatter=json.loads,
)

CELERY_ROUTES = "cms.celery.Router"

# Force accepted content to "json" only. If we also accept pickle-serialized
# messages, the worker will crash when it's running with a privileged user (even
# if it's not the root user but a user belonging to the root group, which is our
# case with OpenShift).
CELERY_ACCEPT_CONTENT = ["json"]

############# NON-SECURE ENV CONFIG ##############################
# Things like server locations, ports, etc.

# GITHUB_REPO_ROOT is the base directory for course data
GITHUB_REPO_ROOT = config(
    "GITHUB_REPO_ROOT", default=path("/edx/app/edxapp/data"), formatter=path
)

# DEFAULT_COURSE_ABOUT_IMAGE_URL specifies the default image to show for
# courses that don't provide one
DEFAULT_COURSE_ABOUT_IMAGE_URL = config(
    "DEFAULT_COURSE_ABOUT_IMAGE_URL", default="images/pencils.jpg"
)

STATIC_URL_BASE = "/static/"
STATIC_URL = "/static/studio/"
STATIC_ROOT_BASE = path("/edx/app/edxapp/staticfiles")
STATIC_ROOT = path("/edx/app/edxapp/staticfiles/studio")
STATICFILES_STORAGE = config(
    "STATICFILES_STORAGE", default="lms.envs.fun.storage.CDNPipelineCachedStorage"
)
CDN_BASE_URL = config("CDN_BASE_URL", default=None)
PIPELINE = True

EMAIL_BACKEND = config(
    "EMAIL_BACKEND", default="django.core.mail.backends.smtp.EmailBackend"
)
EMAIL_FILE_PATH = config("EMAIL_FILE_PATH", default=None)

EMAIL_HOST = config("EMAIL_HOST", default="localhost")
EMAIL_PORT = config("EMAIL_PORT", default=25, formatter=int)
EMAIL_USE_TLS = config("EMAIL_USE_TLS", default=False, formatter=bool)

LMS_BASE = config("LMS_BASE", default="localhost:8072")
CMS_BASE = config("CMS_BASE", default="localhost:8082")

LMS_ROOT_URL = config("LMS_ROOT_URL", default="http://{:s}".format(LMS_BASE))
LMS_INTERNAL_ROOT_URL = config("LMS_INTERNAL_ROOT_URL", default=LMS_ROOT_URL)

SITE_NAME = config("SITE_NAME", default=CMS_BASE)

ALLOWED_HOSTS = config(
    "ALLOWED_HOSTS", default=[CMS_BASE.split(":")[0]], formatter=json.loads
)

LOG_DIR = config("LOG_DIR", default=path("/edx/var/logs/edx"), formatter=path)

MEMCACHED_HOST = config("MEMCACHED_HOST", default="memcached")
MEMCACHED_PORT = config("MEMCACHED_PORT", default=11211, formatter=int)

CACHES = config(
    "CACHES",
    default={
        "default": {
            "BACKEND": "django.core.cache.backends.memcached.MemcachedCache",
            "LOCATION": "{}:{}".format(MEMCACHED_HOST, MEMCACHED_PORT),
            "KEY_FUNCTION": "util.memcache.safe_key",
            "KEY_PREFIX": "default",
        },
        "general": {
            "BACKEND": "django.core.cache.backends.memcached.MemcachedCache",
            "LOCATION": "{}:{}".format(MEMCACHED_HOST, MEMCACHED_PORT),
            "KEY_FUNCTION": "util.memcache.safe_key",
            "KEY_PREFIX": "general",
        },
        "loc_cache": {
            "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
            "LOCATION": "edx_location_mem_cache",
        },
        "celery": {
            "BACKEND": "django.core.cache.backends.memcached.MemcachedCache",
            "LOCATION": "{}:{}".format(MEMCACHED_HOST, MEMCACHED_PORT),
            "KEY_FUNCTION": "util.memcache.safe_key",
            "KEY_PREFIX": "celery",
        },
        "mongo_metadata_inheritance": {
            "BACKEND": "django.core.cache.backends.memcached.MemcachedCache",
            "LOCATION": "{}:{}".format(MEMCACHED_HOST, MEMCACHED_PORT),
            "KEY_FUNCTION": "util.memcache.safe_key",
            "KEY_PREFIX": "mongo_metadata_inheritance",
        },
        "openassessment_submissions": {
            "BACKEND": "django.core.cache.backends.memcached.MemcachedCache",
            "LOCATION": "{}:{}".format(MEMCACHED_HOST, MEMCACHED_PORT),
            "KEY_FUNCTION": "util.memcache.safe_key",
            "KEY_PREFIX": "openassessment_submissions",
        },
        "staticfiles": {
            "BACKEND": "django.core.cache.backends.memcached.MemcachedCache",
            "LOCATION": "{}:{}".format(MEMCACHED_HOST, MEMCACHED_PORT),
            "KEY_FUNCTION": "util.memcache.safe_key",
            "KEY_PREFIX": "staticfiles",
        },
    },
    formatter=json.loads,
)

SESSION_COOKIE_DOMAIN = config("SESSION_COOKIE_DOMAIN", default=None)
SESSION_COOKIE_HTTPONLY = config(
    "SESSION_COOKIE_HTTPONLY", default=True, formatter=bool
)
SESSION_COOKIE_SECURE = config(
    "SESSION_COOKIE_SECURE", default=SESSION_COOKIE_SECURE, formatter=bool
)
SESSION_ENGINE = config(
    "SESSION_ENGINE", default="django.contrib.sessions.backends.cache"
)
SESSION_SAVE_EVERY_REQUEST = config(
    "SESSION_SAVE_EVERY_REQUEST", default=SESSION_SAVE_EVERY_REQUEST, formatter=bool
)

# social sharing settings
SOCIAL_SHARING_SETTINGS = config(
    "SOCIAL_SHARING_SETTINGS", default=SOCIAL_SHARING_SETTINGS, formatter=json.loads
)

REGISTRATION_EMAIL_PATTERNS_ALLOWED = config(
    "REGISTRATION_EMAIL_PATTERNS_ALLOWED", default=None, formatter=json.loads
)

# allow for environments to specify what cookie name our login subsystem should use
# this is to fix a bug regarding simultaneous logins between edx.org and edge.edx.org which can
# happen with some browsers (e.g. Firefox)
if config("SESSION_COOKIE_NAME", default=None):
    # NOTE, there's a bug in Django (http://bugs.python.org/issue18012) which necessitates this
    # being a str()
    SESSION_COOKIE_NAME = str(config("SESSION_COOKIE_NAME"))

# Set the names of cookies shared with the marketing site
# These have the same cookie domain as the session, which in production
# usually includes subdomains.
EDXMKTG_LOGGED_IN_COOKIE_NAME = config(
    "EDXMKTG_LOGGED_IN_COOKIE_NAME", default=EDXMKTG_LOGGED_IN_COOKIE_NAME
)
EDXMKTG_USER_INFO_COOKIE_NAME = config(
    "EDXMKTG_USER_INFO_COOKIE_NAME", default=EDXMKTG_USER_INFO_COOKIE_NAME
)

# Email overrides
DEFAULT_FROM_EMAIL = config("DEFAULT_FROM_EMAIL", default=DEFAULT_FROM_EMAIL)
DEFAULT_FEEDBACK_EMAIL = config(
    "DEFAULT_FEEDBACK_EMAIL", default=DEFAULT_FEEDBACK_EMAIL
)
ADMINS = config("ADMINS", default=ADMINS, formatter=json.loads)
SERVER_EMAIL = config("SERVER_EMAIL", default=SERVER_EMAIL)
MKTG_URLS = config("MKTG_URLS", default=MKTG_URLS, formatter=json.loads)
TECH_SUPPORT_EMAIL = config("TECH_SUPPORT_EMAIL", default=TECH_SUPPORT_EMAIL)

COURSES_WITH_UNSAFE_CODE = config(
    "COURSES_WITH_UNSAFE_CODE", default=[], formatter=json.loads
)

LOCALE_PATHS = config("LOCALE_PATHS", default=LOCALE_PATHS, formatter=json.loads)

ASSET_IGNORE_REGEX = config("ASSET_IGNORE_REGEX", default=ASSET_IGNORE_REGEX)

# Theme overrides
THEME_NAME = config("THEME_NAME", default=None)
COMPREHENSIVE_THEME_DIR = path(
    config("COMPREHENSIVE_THEME_DIR", default=COMPREHENSIVE_THEME_DIR)
)

# Timezone overrides
TIME_ZONE = config("TIME_ZONE", default=TIME_ZONE)

# Push to LMS overrides
GIT_REPO_EXPORT_DIR = config(
    "GIT_REPO_EXPORT_DIR",
    default=path("/edx/var/edxapp/export_course_repos"),
    formatter=path,
)

# Translation overrides
LANGUAGES = config("LANGUAGES", default=LANGUAGES, formatter=json.loads)
LANGUAGE_CODE = config("LANGUAGE_CODE", default=LANGUAGE_CODE)

USE_I18N = config("USE_I18N", default=USE_I18N, formatter=bool)
ALL_LANGUAGES = config("ALL_LANGUAGES", default=ALL_LANGUAGES, formatter=json.loads)

# Override feature by feature by whatever is being redefined in the settings.yaml file
CONFIG_FEATURES = config("FEATURES", default={}, formatter=json.loads)
FEATURES.update(CONFIG_FEATURES)


# Additional installed apps
for app in config("ADDL_INSTALLED_APPS", default=[], formatter=json.loads):
    INSTALLED_APPS.append(app)

WIKI_ENABLED = config("WIKI_ENABLED", default=WIKI_ENABLED, formatter=bool)

# Configure Logging

# Default format for syslog logging
standard_format = "%(asctime)s %(levelname)s %(process)d [%(name)s] %(filename)s:%(lineno)d - %(message)s"
syslog_format = (
    "[variant:cms][%(name)s][env:sandbox] %(levelname)s "
    "[{hostname}  %(process)d] [%(filename)s:%(lineno)d] - %(message)s"
).format(hostname=platform.node().split(".")[0])

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "local": {
            "formatter": "syslog_format",
            "class": "logging.StreamHandler",
            "level": "INFO",
        },
        "tracking": {
            "formatter": "raw",
            "class": "logging.StreamHandler",
            "level": "DEBUG",
        },
        "console": {
            "formatter": "standard",
            "class": "logging.StreamHandler",
            "level": "INFO",
        },
    },
    "formatters": {
        "raw": {"format": "%(message)s"},
        "syslog_format": {"format": syslog_format},
        "standard": {"format": standard_format},
    },
    "filters": {"require_debug_false": {"()": "django.utils.log.RequireDebugFalse"}},
    "loggers": {
        "": {"level": "INFO", "propagate": False, "handlers": ["console", "local"]},
        "tracking": {"level": "DEBUG", "propagate": False, "handlers": ["tracking"]},
    },
}

SENTRY_DSN = config("SENTRY_DSN", default=None)
if SENTRY_DSN:
    LOGGING["loggers"][""]["handlers"].append("sentry")
    LOGGING["handlers"]["sentry"] = {
        "class": "raven.handlers.logging.SentryHandler",
        "dsn": SENTRY_DSN,
        "level": "ERROR",
        "environment": "production",
        "release": RELEASE,
    }

# FIXME: the PLATFORM_NAME and PLATFORM_DESCRIPTION settings should be set to lazy translatable
# strings but edX tries to serialize them with a default json serializer which breaks. We should
# submit a PR to fix it in edx-platform
PLATFORM_NAME = config("PLATFORM_NAME", default="Your Platform Name Here")
PLATFORM_DESCRIPTION = config(
    "PLATFORM_DESCRIPTION", default="Your Platform Description Here"
)
STUDIO_NAME = config("STUDIO_NAME", default=STUDIO_NAME)
STUDIO_SHORT_NAME = config("STUDIO_SHORT_NAME", default=STUDIO_SHORT_NAME)

# Event Tracking
TRACKING_IGNORE_URL_PATTERNS = config(
    "TRACKING_IGNORE_URL_PATTERNS",
    default=TRACKING_IGNORE_URL_PATTERNS,
    formatter=json.loads,
)

# Django CAS external authentication settings
CAS_EXTRA_LOGIN_PARAMS = config(
    "CAS_EXTRA_LOGIN_PARAMS", default=None, formatter=json.loads
)
if FEATURES.get("AUTH_USE_CAS"):
    CAS_SERVER_URL = config("CAS_SERVER_URL", default=None)
    AUTHENTICATION_BACKENDS = [
        "django.contrib.auth.backends.ModelBackend",
        "django_cas.backends.CASBackend",
    ]
    INSTALLED_APPS.append("django_cas")
    MIDDLEWARE_CLASSES.append("django_cas.middleware.CASMiddleware")
    CAS_ATTRIBUTE_CALLBACK = config(
        "CAS_ATTRIBUTE_CALLBACK", default=None, formatter=json.loads
    )
    if CAS_ATTRIBUTE_CALLBACK:
        import importlib

        CAS_USER_DETAILS_RESOLVER = getattr(
            importlib.import_module(CAS_ATTRIBUTE_CALLBACK["module"]),
            CAS_ATTRIBUTE_CALLBACK["function"],
        )

################ SECURE AUTH ITEMS ###############################

############### XBlock filesystem field config ##########
DJFS = config(
    "DJFS",
    default={
        "directory_root": "/edx/var/edxapp/django-pyfs/static/django-pyfs",
        "type": "osfs",
        "url_root": "/static/django-pyfs",
    },
    formatter=json.loads,
)

EMAIL_HOST_USER = config("EMAIL_HOST_USER", default=EMAIL_HOST_USER)
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD", default=EMAIL_HOST_PASSWORD)

# Note that this is the Studio key for Segment. There is a separate key for the LMS.
CMS_SEGMENT_KEY = config("SEGMENT_KEY", default=None)

SECRET_KEY = config("SECRET_KEY", default="ThisIsAnExampleKeyForDevPurposeOnly")

DEFAULT_FILE_STORAGE = config(
    "DEFAULT_FILE_STORAGE", default="django.core.files.storage.FileSystemStorage"
)

# Databases

DATABASE_ENGINE = config("DATABASE_ENGINE", default="django.db.backends.mysql")
DATABASE_HOST = config("DATABASE_HOST", default="mysql")
DATABASE_PORT = config("DATABASE_PORT", default=3306, formatter=int)
DATABASE_NAME = config("DATABASE_NAME", default="edxapp")
DATABASE_USER = config("DATABASE_USER", default="edxapp_user")
DATABASE_PASSWORD = config("DATABASE_PASSWORD", default="password")

DATABASES = config(
    "DATABASES",
    default={
        "default": {
            "ENGINE": DATABASE_ENGINE,
            "HOST": DATABASE_HOST,
            "PORT": DATABASE_PORT,
            "NAME": DATABASE_NAME,
            "USER": DATABASE_USER,
            "PASSWORD": DATABASE_PASSWORD,
        }
    },
    formatter=json.loads,
)

# Enable automatic transaction management on all databases
# https://docs.djangoproject.com/en/1.8/topics/db/transactions/#tying-transactions-to-http-requests
# This needs to be true for all databases
for database_name in DATABASES:
    DATABASES[database_name]["ATOMIC_REQUESTS"] = True

MODULESTORE = convert_module_store_setting_if_needed(
    config("MODULESTORE", default=MODULESTORE, formatter=json.loads)
)

MONGODB_PASSWORD = config("MONGODB_PASSWORD", default="")
MONGODB_HOST = config("MONGODB_HOST", default="mongodb")
MONGODB_PORT = config("MONGODB_PORT", default=27017, formatter=int)
MONGODB_NAME = config("MONGODB_NAME", default="edxapp")
MONGODB_USER = config("MONGODB_USER", default=None)
MONGODB_SSL = config("MONGODB_SSL", default=False, formatter=bool)

DOC_STORE_CONFIG = config(
    "DOC_STORE_CONFIG",
    default={
        "collection": "modulestore",
        "host": MONGODB_HOST,
        "port": MONGODB_PORT,
        "db": MONGODB_NAME,
        "user": MONGODB_USER,
        "password": MONGODB_PASSWORD,
        "ssl": MONGODB_SSL,
    },
    formatter=json.loads,
)

update_module_store_settings(MODULESTORE, doc_store_settings=DOC_STORE_CONFIG)

MONGODB_LOG = config("MONGODB_LOG", default={}, formatter=json.loads)

CONTENTSTORE = config(
    "CONTENTSTORE",
    default={
        "DOC_STORE_CONFIG": DOC_STORE_CONFIG,
        "ENGINE": "xmodule.contentstore.mongo.MongoContentStore",
    },
    formatter=json.loads,
)

# Datadog for events!
DATADOG = config("DATADOG", default={}, formatter=json.loads)

# TODO: deprecated (compatibility with previous settings)
DATADOG["api_key"] = config("DATADOG_API", default=None)

# Celery Broker
CELERY_BROKER_TRANSPORT = config("CELERY_BROKER_TRANSPORT", default="redis")
CELERY_BROKER_USER = config("CELERY_BROKER_USER", default="")
CELERY_BROKER_PASSWORD = config("CELERY_BROKER_PASSWORD", default="")
CELERY_BROKER_HOST = config("CELERY_BROKER_HOST", default="redis")
CELERY_BROKER_PORT = config("CELERY_BROKER_PORT", default=6379, formatter=int)
CELERY_BROKER_VHOST = config("CELERY_BROKER_VHOST", default=0, formatter=int)

BROKER_URL = "{transport}://{user}:{password}@{host}:{port}/{vhost}".format(
    transport=CELERY_BROKER_TRANSPORT,
    user=CELERY_BROKER_USER,
    password=CELERY_BROKER_PASSWORD,
    host=CELERY_BROKER_HOST,
    port=CELERY_BROKER_PORT,
    vhost=CELERY_BROKER_VHOST,
)

# Event tracking
TRACKING_BACKENDS.update(config("TRACKING_BACKENDS", default={}, formatter=json.loads))
EVENT_TRACKING_BACKENDS["tracking_logs"]["OPTIONS"]["backends"].update(
    config("EVENT_TRACKING_BACKENDS", default={}, formatter=json.loads)
)
EVENT_TRACKING_BACKENDS["segmentio"]["OPTIONS"]["processors"][0]["OPTIONS"][
    "whitelist"
].extend(
    config("EVENT_TRACKING_SEGMENTIO_EMIT_WHITELIST", default=[], formatter=json.loads)
)

SUBDOMAIN_BRANDING = config("SUBDOMAIN_BRANDING", default={}, formatter=json.loads)
VIRTUAL_UNIVERSITIES = config("VIRTUAL_UNIVERSITIES", default=[], formatter=json.loads)

##### ACCOUNT LOCKOUT DEFAULT PARAMETERS #####
MAX_FAILED_LOGIN_ATTEMPTS_ALLOWED = config(
    "MAX_FAILED_LOGIN_ATTEMPTS_ALLOWED", default=5, formatter=int
)
MAX_FAILED_LOGIN_ATTEMPTS_LOCKOUT_PERIOD_SECS = config(
    "MAX_FAILED_LOGIN_ATTEMPTS_LOCKOUT_PERIOD_SECS", default=15 * 60, formatter=int
)

MICROSITE_CONFIGURATION = config(
    "MICROSITE_CONFIGURATION", default={}, fomatter=json.loads
)
MICROSITE_ROOT_DIR = path(config("MICROSITE_ROOT_DIR", default=""))

#### PASSWORD POLICY SETTINGS #####
PASSWORD_MIN_LENGTH = config("PASSWORD_MIN_LENGTH", default=12, formatter=int)
PASSWORD_MAX_LENGTH = config("PASSWORD_MAX_LENGTH", default=None, formatter=int)

PASSWORD_COMPLEXITY = config(
    "PASSWORD_COMPLEXITY",
    default={"UPPER": 1, "LOWER": 1, "DIGITS": 1},
    formatter=json.loads,
)
PASSWORD_DICTIONARY_EDIT_DISTANCE_THRESHOLD = config(
    "PASSWORD_DICTIONARY_EDIT_DISTANCE_THRESHOLD",
    default=PASSWORD_DICTIONARY_EDIT_DISTANCE_THRESHOLD,
    formatter=int,
)
PASSWORD_DICTIONARY = config("PASSWORD_DICTIONARY", default=[], formatter=json.loads)

### INACTIVITY SETTINGS ####
SESSION_INACTIVITY_TIMEOUT_IN_SECONDS = config(
    "SESSION_INACTIVITY_TIMEOUT_IN_SECONDS", default=None, formatter=int
)

##### X-Frame-Options response header settings #####
X_FRAME_OPTIONS = config("X_FRAME_OPTIONS", default=X_FRAME_OPTIONS)

##### ADVANCED_SECURITY_CONFIG #####
ADVANCED_SECURITY_CONFIG = config(
    "ADVANCED_SECURITY_CONFIG", default={}, formatter=json.loads
)

################ ADVANCED COMPONENT/PROBLEM TYPES ###############

ADVANCED_COMPONENT_TYPES = config(
    "ADVANCED_COMPONENT_TYPES", default=ADVANCED_COMPONENT_TYPES, formatter=json.loads
)
ADVANCED_PROBLEM_TYPES = config(
    "ADVANCED_PROBLEM_TYPES", default=ADVANCED_PROBLEM_TYPES, formatter=json.loads
)
DEPRECATED_ADVANCED_COMPONENT_TYPES = config(
    "DEPRECATED_ADVANCED_COMPONENT_TYPES",
    default=DEPRECATED_ADVANCED_COMPONENT_TYPES,
    formatter=json.loads,
)

################ VIDEO UPLOAD PIPELINE ###############

VIDEO_UPLOAD_PIPELINE = config(
    "VIDEO_UPLOAD_PIPELINE", default=VIDEO_UPLOAD_PIPELINE, formatter=json.loads
)

################ PUSH NOTIFICATIONS ###############

PARSE_KEYS = config("PARSE_KEYS", default={}, formatter=json.loads)


# Video Caching. Pairing country codes with CDN URLs.
# Example: {'CN': 'http://api.xuetangx.com/edx/video?s3_url='}
VIDEO_CDN_URL = config("VIDEO_CDN_URL", default={}, formatter=json.loads)

if FEATURES["ENABLE_COURSEWARE_INDEX"] or FEATURES["ENABLE_LIBRARY_INDEX"]:
    # Use ElasticSearch for the search engine
    SEARCH_ENGINE = "search.elastic.ElasticSearchEngine"

ELASTIC_SEARCH_CONFIG = config(
    "ELASTIC_SEARCH_CONFIG", default=[{}], formatter=json.loads
)

XBLOCK_SETTINGS = config("XBLOCK_SETTINGS", default={}, formatter=json.loads)
XBLOCK_SETTINGS.setdefault("VideoDescriptor", {})["licensing_enabled"] = FEATURES.get(
    "LICENSING", False
)
XBLOCK_SETTINGS.setdefault("VideoModule", {})["YOUTUBE_API_KEY"] = FEATURES.get(
    "YOUTUBE_API_KEY", YOUTUBE_API_KEY
)

################# PROCTORING CONFIGURATION ##################

PROCTORING_BACKEND_PROVIDER = config(
    "PROCTORING_BACKEND_PROVIDER", default=PROCTORING_BACKEND_PROVIDER
)
PROCTORING_SETTINGS = config(
    "PROCTORING_SETTINGS", default=PROCTORING_SETTINGS, fomatter=json.loads
)

############################ OAUTH2 Provider ###################################

# OpenID Connect issuer ID. Normally the URL of the authentication endpoint.
OAUTH_OIDC_ISSUER = config("OAUTH_OIDC_ISSUER", default=None)
