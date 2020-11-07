"""
This is the settings to run the Open edX CMS with Docker the FUN way.
"""

import json
import os
import platform

from celery_redis_sentinel import register
from lms.envs.fun.utils import Configuration
from openedx.core.lib.derived import derive_settings
from path import Path as path
from xmodule.modulestore.modulestore_settings import (
    convert_module_store_setting_if_needed,
)

from ..common import *


# Load custom configuration parameters from yaml files
config = Configuration(os.path.dirname(__file__))

# edX has now started using "settings.ENV_TOKENS" and "settings.AUTH_TOKENS" everywhere in the
# project, not just in the settings. Let's make sure our settings still work in this case
ENV_TOKENS = config
AUTH_TOKENS = config

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

# Override edX CMS urls with ours
ROOT_URLCONF = "cms.root_urls"

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
# if it's not the root user but a user belonging to the root group, which is the
# case with OpenShift for example).
CELERY_ACCEPT_CONTENT = ["json"]

############# NON-SECURE ENV CONFIG ##############################
# Things like server locations, ports, etc.

# DEFAULT_COURSE_ABOUT_IMAGE_URL specifies the default image to show for courses that don't
# provide one
DEFAULT_COURSE_ABOUT_IMAGE_URL = config(
    "DEFAULT_COURSE_ABOUT_IMAGE_URL", default=DEFAULT_COURSE_ABOUT_IMAGE_URL
)

DEFAULT_COURSE_VISIBILITY_IN_CATALOG = config(
    "DEFAULT_COURSE_VISIBILITY_IN_CATALOG", default=DEFAULT_COURSE_VISIBILITY_IN_CATALOG
)

# DEFAULT_MOBILE_AVAILABLE specifies if the course is available for mobile by default
DEFAULT_MOBILE_AVAILABLE = config(
    "DEFAULT_MOBILE_AVAILABLE", default=DEFAULT_MOBILE_AVAILABLE, formatter=bool
)

# GITHUB_REPO_ROOT is the base directory
# for course data
GITHUB_REPO_ROOT = config("GITHUB_REPO_ROOT", default=GITHUB_REPO_ROOT)

STATIC_URL = "/static/studio/"
STATIC_ROOT_BASE = path("/edx/app/edxapp/staticfiles")
STATIC_ROOT = path("/edx/app/edxapp/staticfiles/studio")
STATICFILES_STORAGE = config(
    "STATICFILES_STORAGE", default="lms.envs.fun.storage.CDNProductionStorage"
)
CDN_BASE_URL = config("CDN_BASE_URL", default=None)

WEBPACK_LOADER["DEFAULT"]["STATS_FILE"] = STATIC_ROOT / "webpack-stats.json"

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
ENTERPRISE_API_URL = config(
    "ENTERPRISE_API_URL", default=LMS_INTERNAL_ROOT_URL + "/enterprise/api/v1/"
)
ENTERPRISE_CONSENT_API_URL = config(
    "ENTERPRISE_CONSENT_API_URL", default=LMS_INTERNAL_ROOT_URL + "/consent/api/v1/"
)

SITE_NAME = config("SITE_NAME", default=CMS_BASE)

ALLOWED_HOSTS = config(
    "ALLOWED_HOSTS", default=[CMS_BASE.split(":")[0]], formatter=json.loads
)

LOG_DIR = config("LOG_DIR", default=path("/edx/var/logs/edx"), formatter=path)

CACHE_REDIS_HOST = config("CACHE_REDIS_HOST", default="redis")
CACHE_REDIS_PORT = config("CACHE_REDIS_PORT", default=6379, formatter=int)
CACHE_REDIS_DB = config("CACHE_REDIS_DB", default=1, formatter=int)
CACHE_REDIS_BACKEND = config(
    "CACHE_REDIS_BACKEND", default="django_redis.cache.RedisCache"
)
CACHE_REDIS_URI = "redis://{}:{}/{}".format(
    CACHE_REDIS_HOST, CACHE_REDIS_PORT, CACHE_REDIS_DB
)
CACHE_REDIS_CLIENT = config(
    "CACHE_REDIS_CLIENT", default="django_redis.client.DefaultClient"
)

CACHES_DEFAULT_CONFIG = {
    "BACKEND": CACHE_REDIS_BACKEND,
    "LOCATION": CACHE_REDIS_URI,
    "OPTIONS": {"CLIENT_CLASS": CACHE_REDIS_CLIENT},
}

if "Sentinel" in CACHE_REDIS_BACKEND:
    CACHES_DEFAULT_CONFIG["LOCATION"] = [(CACHE_REDIS_HOST, CACHE_REDIS_PORT)]
    CACHES_DEFAULT_CONFIG["OPTIONS"]["SENTINEL_SERVICE_NAME"] = config(
        "CACHE_REDIS_SENTINEL_SERVICE_NAME", default="mymaster"
    )
    CACHES_DEFAULT_CONFIG["OPTIONS"]["REDIS_CLIENT_KWARGS"] = {"db": CACHE_REDIS_DB}

CACHES = config(
    "CACHES",
    default={
        "default": dict(CACHES_DEFAULT_CONFIG, **{"KEY_PREFIX": "default"}),
        "general": dict(CACHES_DEFAULT_CONFIG, **{"KEY_PREFIX": "general"}),
        "celery": dict(CACHES_DEFAULT_CONFIG, **{"KEY_PREFIX": "celery"}),
        "mongo_metadata_inheritance": dict(
            CACHES_DEFAULT_CONFIG, **{"KEY_PREFIX": "mongo_metadata_inheritance"}
        ),
        "openassessment_submissions": dict(
            CACHES_DEFAULT_CONFIG, **{"KEY_PREFIX": "openassessment_submissions"}
        ),
        "loc_cache": {
            "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
            "LOCATION": "edx_location_mem_cache",
        },
        # Cache backend used by Django 1.8 storage backend while processing static files
        "staticfiles": {
            "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
            "LOCATION": "edx_location_mem_cache",
        },
    },
    formatter=json.loads,
)

SESSION_COOKIE_DOMAIN = config("SESSION_COOKIE_DOMAIN", default=None)
SESSION_COOKIE_HTTPONLY = config(
    "SESSION_COOKIE_HTTPONLY", default=True, formatter=bool
)
SESSION_ENGINE = config("SESSION_ENGINE", default="redis_sessions.session")

SESSION_COOKIE_SECURE = config(
    "SESSION_COOKIE_SECURE", default=SESSION_COOKIE_SECURE, formatter=bool
)
SESSION_SAVE_EVERY_REQUEST = config(
    "SESSION_SAVE_EVERY_REQUEST", default=SESSION_SAVE_EVERY_REQUEST, formatter=bool
)

SESSION_REDIS_HOST = config("SESSION_REDIS_HOST", default="redis")
SESSION_REDIS_PORT = config("SESSION_REDIS_PORT", default=6379, formatter=int)
SESSION_REDIS_DB = config("SESSION_REDIS_DB", default=1, formatter=int)
SESSION_REDIS_PASSWORD = config("SESSION_REDIS_PASSWORD", default=None)
SESSION_REDIS_PREFIX = config("SESSION_REDIS_PREFIX", default="session")
SESSION_REDIS_SOCKET_TIMEOUT = config(
    "SESSION_REDIS_SOCKET_TIMEOUT", default=1, formatter=int
)
SESSION_REDIS_RETRY_ON_TIMEOUT = config(
    "SESSION_REDIS_RETRY_ON_TIMEOUT", default=False, formatter=bool
)

SESSION_REDIS = config(
    "SESSION_REDIS",
    default={
        "host": SESSION_REDIS_HOST,
        "port": SESSION_REDIS_PORT,
        "db": SESSION_REDIS_DB,  # db 0 is used for Celery Broker
        "password": SESSION_REDIS_PASSWORD,
        "prefix": SESSION_REDIS_PREFIX,
        "socket_timeout": SESSION_REDIS_SOCKET_TIMEOUT,
        "retry_on_timeout": SESSION_REDIS_RETRY_ON_TIMEOUT,
    },
    formatter=json.loads,
)
SESSION_REDIS_SENTINEL_LIST = config(
    "SESSION_REDIS_SENTINEL_LIST", default=None, formatter=json.loads
)
SESSION_REDIS_SENTINEL_MASTER_ALIAS = config(
    "SESSION_REDIS_SENTINEL_MASTER_ALIAS", default=None
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

# Determines whether the CSRF token can be transported on
# unencrypted channels. It is set to False here for backward compatibility,
# but it is highly recommended that this is True for environments accessed
# by end users.
CSRF_COOKIE_SECURE = config("CSRF_COOKIE_SECURE", default=False, formatter=bool)

# Email overrides
DEFAULT_FROM_EMAIL = config("DEFAULT_FROM_EMAIL", default=DEFAULT_FROM_EMAIL)
DEFAULT_FEEDBACK_EMAIL = config(
    "DEFAULT_FEEDBACK_EMAIL", default=DEFAULT_FEEDBACK_EMAIL
)
ADMINS = config("ADMINS", default=ADMINS, formatter=json.loads)
SERVER_EMAIL = config("SERVER_EMAIL", default=SERVER_EMAIL)
MKTG_URLS = config("MKTG_URLS", default=MKTG_URLS, formatter=json.loads)
TECH_SUPPORT_EMAIL = config("TECH_SUPPORT_EMAIL", default=TECH_SUPPORT_EMAIL)

for name, value in config("CODE_JAIL", default={}, formatter=json.loads).items():
    oldvalue = CODE_JAIL.get(name)
    if isinstance(oldvalue, dict):
        for subname, subvalue in value.items():
            oldvalue[subname] = subvalue
    else:
        CODE_JAIL[name] = value

COURSES_WITH_UNSAFE_CODE = config(
    "COURSES_WITH_UNSAFE_CODE", default=[], formatter=json.loads
)

ASSET_IGNORE_REGEX = config("ASSET_IGNORE_REGEX", default=ASSET_IGNORE_REGEX)

COMPREHENSIVE_THEME_DIRS = (
    config(
        "COMPREHENSIVE_THEME_DIRS",
        default=COMPREHENSIVE_THEME_DIRS,
        formatter=json.loads,
    )
    or []
)

LOCALE_PATHS = config("LOCALE_PATHS", default=LOCALE_PATHS, formatter=json.loads)

# COMPREHENSIVE_THEME_LOCALE_PATHS contain the paths to themes locale directories e.g.
# "COMPREHENSIVE_THEME_LOCALE_PATHS" : [
#        "/edx/src/edx-themes/conf/locale"
#    ],
COMPREHENSIVE_THEME_LOCALE_PATHS = config(
    "COMPREHENSIVE_THEME_LOCALE_PATHS", default=[], formatter=json.loads
)

DEFAULT_SITE_THEME = config("DEFAULT_SITE_THEME", default=DEFAULT_SITE_THEME)
ENABLE_COMPREHENSIVE_THEMING = config(
    "ENABLE_COMPREHENSIVE_THEMING", default=ENABLE_COMPREHENSIVE_THEMING, formatter=bool
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
LANGUAGE_COOKIE = config("LANGUAGE_COOKIE", default=LANGUAGE_COOKIE)

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

# Heartbeat
HEARTBEAT_CHECKS = config(
    "HEARTBEAT_CHECKS", default=HEARTBEAT_CHECKS, formatter=json.loads
)
HEARTBEAT_EXTENDED_CHECKS = config(
    "HEARTBEAT_EXTENDED_CHECKS", default=HEARTBEAT_EXTENDED_CHECKS, formatter=json.loads
)
HEARTBEAT_CELERY_TIMEOUT = config(
    "HEARTBEAT_CELERY_TIMEOUT", default=HEARTBEAT_CELERY_TIMEOUT, formatter=int
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

# Specific setting for the File Upload Service to store media in a bucket.
FILE_UPLOAD_STORAGE_BUCKET_NAME = config(
    "FILE_UPLOAD_STORAGE_BUCKET_NAME", default="uploads"
)
FILE_UPLOAD_STORAGE_PREFIX = config(
    "FILE_UPLOAD_STORAGE_PREFIX", default=FILE_UPLOAD_STORAGE_PREFIX
)

# Zendesk
ZENDESK_URL = config("ZENDESK_URL", default=ZENDESK_URL)
ZENDESK_CUSTOM_FIELDS = config(
    "ZENDESK_CUSTOM_FIELDS", default=ZENDESK_CUSTOM_FIELDS, formatter=json.loads
)

################ SECURE AUTH ITEMS ###############################

############### XBlock filesystem field config ##########
DJFS = config("DJFS", default=None, formatter=json.loads)

EMAIL_HOST_USER = config("EMAIL_HOST_USER", default=EMAIL_HOST_USER)
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD", default=EMAIL_HOST_PASSWORD)

# Note that this is the Studio key for Segment. There is a separate key for the LMS.
CMS_SEGMENT_KEY = config("SEGMENT_KEY", default=None)

SECRET_KEY = config("SECRET_KEY", default="ThisIsAnExampleKeyForDevPurposeOnly")

DEFAULT_FILE_STORAGE = config(
    "DEFAULT_FILE_STORAGE", default="django.core.files.storage.FileSystemStorage"
)

USER_TASKS_ARTIFACT_STORAGE = COURSE_IMPORT_EXPORT_STORAGE

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

# Configure the MODULESTORE
MODULESTORE = convert_module_store_setting_if_needed(
    config("MODULESTORE", default=MODULESTORE, formatter=json.loads)
)

MONGODB_PASSWORD = config("MONGODB_PASSWORD", default="")
MONGODB_HOST = config("MONGODB_HOST", default="mongodb")
MONGODB_PORT = config("MONGODB_PORT", default=27017, formatter=int)
MONGODB_NAME = config("MONGODB_NAME", default="edxapp")
MONGODB_USER = config("MONGODB_USER", default=None)
MONGODB_SSL = config("MONGODB_SSL", default=False, formatter=bool)
MONGODB_REPLICASET = config("MONGODB_REPLICASET", default=None)
# Accepted read_preference value can be found here https://github.com/mongodb/mongo-python-driver/blob/2.9.1/pymongo/read_preferences.py#L54
MONGODB_READ_PREFERENCE = config("MONGODB_READ_PREFERENCE", default="PRIMARY")

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
        "replicaSet": MONGODB_REPLICASET,
        "read_preference": MONGODB_READ_PREFERENCE,
    },
    formatter=json.loads,
)

MODULESTORE_FIELD_OVERRIDE_PROVIDERS = config(
    "MODULESTORE_FIELD_OVERRIDE_PROVIDERS",
    default=MODULESTORE_FIELD_OVERRIDE_PROVIDERS,
    formatter=json.loads,
)

XBLOCK_FIELD_DATA_WRAPPERS = config(
    "XBLOCK_FIELD_DATA_WRAPPERS",
    default=XBLOCK_FIELD_DATA_WRAPPERS,
    formatter=json.loads,
)

CONTENTSTORE = config(
    "CONTENTSTORE",
    default={
        "DOC_STORE_CONFIG": DOC_STORE_CONFIG,
        "ENGINE": "xmodule.contentstore.mongo.MongoContentStore",
    },
    formatter=json.loads,
)

update_module_store_settings(MODULESTORE, doc_store_settings=DOC_STORE_CONFIG)

# Datadog for events!
DATADOG = config("DATADOG", default={}, formatter=json.loads)

# TODO: deprecated (compatibility with previous settings)
DATADOG["api_key"] = config("DATADOG_API", default=None)

# Celery Broker
# For redis sentinel use the `redis-sentinel` transport
CELERY_BROKER_TRANSPORT = config("CELERY_BROKER_TRANSPORT", default="redis")
CELERY_BROKER_USER = config("CELERY_BROKER_USER", default="")
CELERY_BROKER_PASSWORD = config("CELERY_BROKER_PASSWORD", default="")
CELERY_BROKER_HOST = config("CELERY_BROKER_HOST", default="redis")
CELERY_BROKER_PORT = config("CELERY_BROKER_PORT", default=6379, formatter=int)
CELERY_BROKER_VHOST = config("CELERY_BROKER_VHOST", default=0, formatter=int)

if CELERY_BROKER_TRANSPORT == "redis-sentinel":
    # register redis sentinel schema in celery
    register()

BROKER_URL = "{transport}://{user}:{password}@{host}:{port}/{vhost}".format(
    transport=CELERY_BROKER_TRANSPORT,
    user=CELERY_BROKER_USER,
    password=CELERY_BROKER_PASSWORD,
    host=CELERY_BROKER_HOST,
    port=CELERY_BROKER_PORT,
    vhost=CELERY_BROKER_VHOST,
)
BROKER_USE_SSL = config("CELERY_BROKER_USE_SSL", default=False, formatter=bool)
# To use redis-sentinel, refer to the documentation here
# https://celery-redis-sentinel.readthedocs.io/en/latest/
BROKER_TRANSPORT_OPTIONS = config(
    "BROKER_TRANSPORT_OPTIONS", default={}, formatter=json.loads
)

# Message expiry time in seconds
CELERY_EVENT_QUEUE_TTL = config("CELERY_EVENT_QUEUE_TTL", default=None, formatter=int)

# Queue to use for updating grades due to grading policy change
POLICY_CHANGE_GRADES_ROUTING_KEY = config(
    "POLICY_CHANGE_GRADES_ROUTING_KEY", default=LOW_PRIORITY_QUEUE
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

##### ORA2 ######
ORA2_FILEUPLOAD_BACKEND = config("ORA2_FILEUPLOAD_BACKEND", default="filesystem")

# Prefix for uploads of example-based assessment AI classifiers
# This can be used to separate uploads for different environments
ORA2_FILE_PREFIX = config("ORA2_FILE_PREFIX", default=None)

# If backend is "filesystem"
ORA2_FILEUPLOAD_ROOT = DATA_DIR / "openassessment_submissions"
ORA2_FILEUPLOAD_CACHE_NAME = config(
    "ORA2_FILEUPLOAD_CACHE_NAME", default="openassessment_submissions"
)

# If backend is "swift"
ORA2_SWIFT_KEY = config("ORA2_SWIFT_KEY", default="")
ORA2_SWIFT_URL = config("ORA2_SWIFT_URL", default="")

##### ACCOUNT LOCKOUT DEFAULT PARAMETERS #####
MAX_FAILED_LOGIN_ATTEMPTS_ALLOWED = config(
    "MAX_FAILED_LOGIN_ATTEMPTS_ALLOWED", default=5, formatter=int
)
MAX_FAILED_LOGIN_ATTEMPTS_LOCKOUT_PERIOD_SECS = config(
    "MAX_FAILED_LOGIN_ATTEMPTS_LOCKOUT_PERIOD_SECS", default=15 * 60, formatter=int
)

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

ADVANCED_PROBLEM_TYPES = config(
    "ADVANCED_PROBLEM_TYPES", default=ADVANCED_PROBLEM_TYPES, formatter=json.loads
)

################ VIDEO UPLOAD PIPELINE ###############

VIDEO_UPLOAD_PIPELINE = config(
    "VIDEO_UPLOAD_PIPELINE", default=VIDEO_UPLOAD_PIPELINE, formatter=json.loads
)

################ VIDEO IMAGE STORAGE ###############

VIDEO_IMAGE_SETTINGS = config(
    "VIDEO_IMAGE_SETTINGS", default=VIDEO_IMAGE_SETTINGS, formatter=json.loads
)

################ VIDEO TRANSCRIPTS STORAGE ###############

VIDEO_TRANSCRIPTS_SETTINGS = config(
    "VIDEO_TRANSCRIPTS_SETTINGS",
    default=VIDEO_TRANSCRIPTS_SETTINGS,
    formatter=json.loads,
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

################ CONFIGURABLE LTI CONSUMER ###############

# Add just the standard LTI consumer by default, forcing it to open in a new window and ask
# the user before sending email and username:
LTI_XBLOCK_CONFIGURATIONS = config(
    "LTI_XBLOCK_CONFIGURATIONS",
    default=[
        {
            "display_name": "LTI consumer",
            "pattern": ".*",
            "hidden_fields": [
                "ask_to_send_email",
                "ask_to_send_username",
                "new_window",
            ],
            "defaults": {
                "ask_to_send_email": True,
                "ask_to_send_username": True,
                "launch_target": "new_window",
            },
        }
    ],
    formatter=json.loads,
)
LTI_XBLOCK_SECRETS = config("LTI_XBLOCK_SECRETS", default={}, formatter=json.loads)

XBLOCK_SETTINGS = config("XBLOCK_SETTINGS", default={}, formatter=json.loads)
XBLOCK_SETTINGS.setdefault("VideoDescriptor", {})["licensing_enabled"] = FEATURES.get(
    "LICENSING", False
)
XBLOCK_SETTINGS.setdefault("VideoModule", {})["YOUTUBE_API_KEY"] = config(
    "YOUTUBE_API_KEY", default=YOUTUBE_API_KEY
)

################# PROCTORING CONFIGURATION ##################

PROCTORING_BACKEND_PROVIDER = config(
    "PROCTORING_BACKEND_PROVIDER", default=PROCTORING_BACKEND_PROVIDER
)
PROCTORING_SETTINGS = config(
    "PROCTORING_SETTINGS", default=PROCTORING_SETTINGS, formatter=json.loads
)

################# MICROSITE ####################
# microsite specific configurations.
MICROSITE_CONFIGURATION = config(
    "MICROSITE_CONFIGURATION", default={}, formatter=json.loads
)
MICROSITE_ROOT_DIR = path(config("MICROSITE_ROOT_DIR", default=""))
# this setting specify which backend to be used when pulling microsite specific configuration
MICROSITE_BACKEND = config("MICROSITE_BACKEND", default=MICROSITE_BACKEND)
# this setting specify which backend to be used when loading microsite specific templates
MICROSITE_TEMPLATE_BACKEND = config(
    "MICROSITE_TEMPLATE_BACKEND", default=MICROSITE_TEMPLATE_BACKEND
)
# TTL for microsite database template cache
MICROSITE_DATABASE_TEMPLATE_CACHE_TTL = config(
    "MICROSITE_DATABASE_TEMPLATE_CACHE_TTL",
    default=MICROSITE_DATABASE_TEMPLATE_CACHE_TTL,
    formatter=int,
)

############################ OAUTH2 Provider ###################################

# OpenID Connect issuer ID. Normally the URL of the authentication endpoint.
OAUTH_OIDC_ISSUER = config("OAUTH_OIDC_ISSUER", default=None)

#### JWT configuration ####
JWT_AUTH.update(config("JWT_AUTH", default={}, formatter=json.loads))

######################## CUSTOM COURSES for EDX CONNECTOR ######################
if FEATURES.get("CUSTOM_COURSES_EDX"):
    INSTALLED_APPS.append("openedx.core.djangoapps.ccxcon.apps.CCXConnectorConfig")

# Partner support link for CMS footer
PARTNER_SUPPORT_EMAIL = config("PARTNER_SUPPORT_EMAIL", default=PARTNER_SUPPORT_EMAIL)

# Affiliate cookie tracking
AFFILIATE_COOKIE_NAME = config("AFFILIATE_COOKIE_NAME", default=AFFILIATE_COOKIE_NAME)

############## Settings for Studio Context Sensitive Help ##############

HELP_TOKENS_BOOKS = config(
    "HELP_TOKENS_BOOKS", default=HELP_TOKENS_BOOKS, formatter=json.loads
)

############## Settings for CourseGraph ############################
COURSEGRAPH_JOB_QUEUE = config("COURSEGRAPH_JOB_QUEUE", default=LOW_PRIORITY_QUEUE)

########################## Parental controls config  #######################

# The age at which a learner no longer requires parental consent, or None
# if parental consent is never required.
PARENTAL_CONSENT_AGE_LIMIT = config(
    "PARENTAL_CONSENT_AGE_LIMIT", default=PARENTAL_CONSENT_AGE_LIMIT, formatter=int
)

########################## Extra middleware classes  #######################

# Allow extra middleware classes to be added to the app through configuration.
MIDDLEWARE_CLASSES.extend(
    config("EXTRA_MIDDLEWARE_CLASSES", default=[], formatter=json.loads)
)

########################## Settings for Completion API #####################

# Once a user has watched this percentage of a video, mark it as complete:
# (0.0 = 0%, 1.0 = 100%)
COMPLETION_VIDEO_COMPLETE_PERCENTAGE = config(
    "COMPLETION_VIDEO_COMPLETE_PERCENTAGE",
    default=COMPLETION_VIDEO_COMPLETE_PERCENTAGE,
    formatter=float,
)

####################### Enterprise Settings ######################
# A shared secret to be used for encrypting passwords passed from the enterprise api
# to the enteprise reporting script.
ENTERPRISE_REPORTING_SECRET = config(
    "ENTERPRISE_REPORTING_SECRET", default=ENTERPRISE_REPORTING_SECRET
)

############### Settings for Retirement #####################
RETIRED_USERNAME_PREFIX = config(
    "RETIRED_USERNAME_PREFIX", default=RETIRED_USERNAME_PREFIX
)
RETIRED_EMAIL_PREFIX = config("RETIRED_EMAIL_PREFIX", default=RETIRED_EMAIL_PREFIX)
RETIRED_EMAIL_DOMAIN = config("RETIRED_EMAIL_DOMAIN", default=RETIRED_EMAIL_DOMAIN)
RETIREMENT_SERVICE_WORKER_USERNAME = config(
    "RETIREMENT_SERVICE_WORKER_USERNAME", default=RETIREMENT_SERVICE_WORKER_USERNAME
)
RETIREMENT_STATES = config(
    "RETIREMENT_STATES", default=RETIREMENT_STATES, formatter=json.loads
)

####################### Plugin Settings ##########################

from openedx.core.djangoapps.plugins import (
    plugin_settings,
    constants as plugin_constants,
)

plugin_settings.add_plugins(
    __name__, plugin_constants.ProjectType.CMS, plugin_constants.SettingsType.AWS
)

########################## Derive Any Derived Settings  #######################

derive_settings(__name__)
