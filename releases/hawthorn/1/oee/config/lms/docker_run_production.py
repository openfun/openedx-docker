# -*- coding: utf-8 -*-

"""
This is the settings to run Open edX with Docker the FUN way.
"""

import datetime
import dateutil
import json
import os
import platform

from celery_redis_sentinel import register
from openedx.core.lib.derived import derive_settings
from path import Path as path
from xmodule.modulestore.modulestore_settings import (
    convert_module_store_setting_if_needed,
)

from ..common import *
from .utils import Configuration

# Load custom configuration parameters from yaml files
config = Configuration(os.path.dirname(__file__))

# edX has now started using "settings.ENV_TOKENS" and "settings.AUTH_TOKENS" everywhere in the
# project, not just in the settings. Let's make sure our settings still work in this case
ENV_TOKENS = config
AUTH_TOKENS = config

################################ ALWAYS THE SAME ##############################

RELEASE = config("RELEASE", default=None)
DEBUG = False
DEFAULT_TEMPLATE_ENGINE["OPTIONS"]["debug"] = False

SESSION_ENGINE = config("SESSION_ENGINE", default="redis_sessions.session")

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

# Override edX LMS urls with ours
ROOT_URLCONF = "lms.root_urls"

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

# Celery queues

DEFAULT_PRIORITY_QUEUE = config(
    "DEFAULT_PRIORITY_QUEUE", default="edx.lms.core.default"
)
HIGH_PRIORITY_QUEUE = config("HIGH_PRIORITY_QUEUE", default="edx.lms.core.high")
LOW_PRIORITY_QUEUE = config("LOW_PRIORITY_QUEUE", default="edx.lms.core.low")
HIGH_MEM_QUEUE = config("HIGH_MEM_QUEUE", default="edx.lms.core.high_mem")

CELERY_DEFAULT_QUEUE = DEFAULT_PRIORITY_QUEUE
CELERY_DEFAULT_ROUTING_KEY = DEFAULT_PRIORITY_QUEUE

CELERY_QUEUES = config(
    "CELERY_QUEUES",
    default={
        DEFAULT_PRIORITY_QUEUE: {},
        HIGH_PRIORITY_QUEUE: {},
        LOW_PRIORITY_QUEUE: {},
        HIGH_MEM_QUEUE: {},
    },
    formatter=json.loads,
)

CELERY_ROUTES = "lms.celery.Router"

# Force accepted content to "json" only. If we also accept pickle-serialized
# messages, the worker will crash when it's running with a privileged user (even
# if it's not the root user but a user belonging to the root group, which is our
# case with OpenShift).
CELERY_ACCEPT_CONTENT = ["json"]

CELERYBEAT_SCHEDULE = {}  # For scheduling tasks, entries can be added to this dict

########################## NON-SECURE ENV CONFIG ##############################
# Things like server locations, ports, etc.

STATIC_ROOT_BASE = path("/edx/app/edxapp/staticfiles")
STATIC_ROOT = STATIC_ROOT_BASE
STATIC_URL = "/static/"
STATICFILES_STORAGE = config(
    "STATICFILES_STORAGE", default="lms.envs.fun.storage.CDNProductionStorage"
)
CDN_BASE_URL = config("CDN_BASE_URL", default=None)

WEBPACK_LOADER["DEFAULT"]["STATS_FILE"] = STATIC_ROOT / "webpack-stats.json"

MEDIA_ROOT = path("/edx/var/edxapp/media/")
MEDIA_URL = "/media/"

LOG_DIR = config("LOG_DIR", default=path("/edx/var/logs/edx"), formatter=path)
DATA_DIR = config("DATA_DIR", default=path("/edx/app/edxapp/data"), formatter=path)

# DEFAULT_COURSE_ABOUT_IMAGE_URL specifies the default image to show for courses that don't provide one
DEFAULT_COURSE_ABOUT_IMAGE_URL = config(
    "DEFAULT_COURSE_ABOUT_IMAGE_URL", default=DEFAULT_COURSE_ABOUT_IMAGE_URL
)

# COURSE_MODE_DEFAULTS specifies the course mode to use for courses that do not set one
COURSE_MODE_DEFAULTS = config(
    "COURSE_MODE_DEFAULTS", default=COURSE_MODE_DEFAULTS, formatter=json.loads
)

# FIXME: the PLATFORM_NAME and PLATFORM_DESCRIPTION settings should be set to lazy translatable
# strings but edX tries to serialize them with a default json serializer which breaks. We should
# submit a PR to fix it in edx-platform
PLATFORM_NAME = config("PLATFORM_NAME", default="Your Platform Name Here")
PLATFORM_DESCRIPTION = config(
    "PLATFORM_DESCRIPTION", default="Your Platform Description Here"
)
PLATFORM_TWITTER_ACCOUNT = config(
    "PLATFORM_TWITTER_ACCOUNT", default=PLATFORM_TWITTER_ACCOUNT
)
PLATFORM_FACEBOOK_ACCOUNT = config(
    "PLATFORM_FACEBOOK_ACCOUNT", default=PLATFORM_FACEBOOK_ACCOUNT
)
SOCIAL_SHARING_SETTINGS = config(
    "SOCIAL_SHARING_SETTINGS", default=SOCIAL_SHARING_SETTINGS, formatter=json.loads
)

# Social media links for the page footer
SOCIAL_MEDIA_FOOTER_URLS = config(
    "SOCIAL_MEDIA_FOOTER_URLS", default=SOCIAL_MEDIA_FOOTER_URLS, formatter=json.loads
)

CC_MERCHANT_NAME = config("CC_MERCHANT_NAME", default=PLATFORM_NAME)
EMAIL_BACKEND = config(
    "EMAIL_BACKEND", default="django.core.mail.backends.smtp.EmailBackend"
)
EMAIL_FILE_PATH = config("EMAIL_FILE_PATH", default=None)
EMAIL_HOST = config("EMAIL_HOST", default="localhost")
EMAIL_PORT = config("EMAIL_PORT", default=25, formatter=int)
EMAIL_USE_TLS = config("EMAIL_USE_TLS", default=False, formatter=bool)
HTTPS = config("HTTPS", default=HTTPS)
SESSION_COOKIE_DOMAIN = config("SESSION_COOKIE_DOMAIN", default=None)
SESSION_COOKIE_HTTPONLY = config(
    "SESSION_COOKIE_HTTPONLY", default=True, formatter=bool
)
SESSION_COOKIE_SECURE = config(
    "SESSION_COOKIE_SECURE", default=SESSION_COOKIE_SECURE, formatter=bool
)
SESSION_SAVE_EVERY_REQUEST = config(
    "SESSION_SAVE_EVERY_REQUEST", default=SESSION_SAVE_EVERY_REQUEST, formatter=bool
)

REGISTRATION_EXTRA_FIELDS = config(
    "REGISTRATION_EXTRA_FIELDS", default=REGISTRATION_EXTRA_FIELDS, formatter=json.loads
)
REGISTRATION_EXTENSION_FORM = config(
    "REGISTRATION_EXTENSION_FORM", default=REGISTRATION_EXTENSION_FORM
)
REGISTRATION_EMAIL_PATTERNS_ALLOWED = config(
    "REGISTRATION_EMAIL_PATTERNS_ALLOWED", default=None, formatter=json.loads
)
REGISTRATION_FIELD_ORDER = config(
    "REGISTRATION_FIELD_ORDER", default=REGISTRATION_FIELD_ORDER, formatter=json.loads
)

# Set the names of cookies shared with the marketing site
# These have the same cookie domain as the session, which in production
# usually includes subdomains.
EDXMKTG_LOGGED_IN_COOKIE_NAME = config(
    "EDXMKTG_LOGGED_IN_COOKIE_NAME", default=EDXMKTG_LOGGED_IN_COOKIE_NAME
)
EDXMKTG_USER_INFO_COOKIE_NAME = config(
    "EDXMKTG_USER_INFO_COOKIE_NAME", default=EDXMKTG_USER_INFO_COOKIE_NAME
)

# Override feature by feature by whatever is being redefined in the settings.yaml file
CONFIG_FEATURES = config("FEATURES", default={}, formatter=json.loads)
FEATURES.update(CONFIG_FEATURES)

LMS_BASE = config("LMS_BASE", default="localhost:8072")
CMS_BASE = config("CMS_BASE", default="localhost:8082")

LMS_ROOT_URL = config("LMS_ROOT_URL", default="http://{:s}".format(LMS_BASE))
LMS_INTERNAL_ROOT_URL = config("LMS_INTERNAL_ROOT_URL", default=LMS_ROOT_URL)

SITE_NAME = config("SITE_NAME", default=LMS_BASE)

ALLOWED_HOSTS = config(
    "ALLOWED_HOSTS", default=[LMS_BASE.split(":")[0]], formatter=json.loads
)
if FEATURES.get("PREVIEW_LMS_BASE"):
    ALLOWED_HOSTS.append(FEATURES["PREVIEW_LMS_BASE"])

# allow for environments to specify what cookie name our login subsystem should use
# this is to fix a bug regarding simultaneous logins between edx.org and edge.edx.org which can
# happen with some browsers (e.g. Firefox)
if config("SESSION_COOKIE_NAME", default=None):
    # NOTE, there's a bug in Django (http://bugs.python.org/issue18012) which necessitates this
    # being a str()
    SESSION_COOKIE_NAME = str(config("SESSION_COOKIE_NAME"))

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

# Email overrides
DEFAULT_FROM_EMAIL = config("DEFAULT_FROM_EMAIL", default=DEFAULT_FROM_EMAIL)
DEFAULT_FEEDBACK_EMAIL = config(
    "DEFAULT_FEEDBACK_EMAIL", default=DEFAULT_FEEDBACK_EMAIL
)
ADMINS = config("ADMINS", default=ADMINS, formatter=json.loads)
SERVER_EMAIL = config("SERVER_EMAIL", default=SERVER_EMAIL)
TECH_SUPPORT_EMAIL = config("TECH_SUPPORT_EMAIL", default=TECH_SUPPORT_EMAIL)
CONTACT_EMAIL = config("CONTACT_EMAIL", default=CONTACT_EMAIL)
BUGS_EMAIL = config("BUGS_EMAIL", default=BUGS_EMAIL)
PAYMENT_SUPPORT_EMAIL = config("PAYMENT_SUPPORT_EMAIL", default=PAYMENT_SUPPORT_EMAIL)
FINANCE_EMAIL = config("FINANCE_EMAIL", default=FINANCE_EMAIL)
UNIVERSITY_EMAIL = config("UNIVERSITY_EMAIL", default=UNIVERSITY_EMAIL)
PRESS_EMAIL = config("PRESS_EMAIL", default=PRESS_EMAIL)

CONTACT_MAILING_ADDRESS = config(
    "CONTACT_MAILING_ADDRESS", default=CONTACT_MAILING_ADDRESS
)

# Account activation email sender address
ACTIVATION_EMAIL_FROM_ADDRESS = config(
    "ACTIVATION_EMAIL_FROM_ADDRESS", default=DEFAULT_FROM_EMAIL
)

# Currency
PAID_COURSE_REGISTRATION_CURRENCY = config(
    "PAID_COURSE_REGISTRATION_CURRENCY", default=PAID_COURSE_REGISTRATION_CURRENCY
)

# Payment Report Settings
PAYMENT_REPORT_GENERATOR_GROUP = config(
    "PAYMENT_REPORT_GENERATOR_GROUP", default=PAYMENT_REPORT_GENERATOR_GROUP
)

# Bulk Email overrides
BULK_EMAIL_DEFAULT_FROM_EMAIL = config(
    "BULK_EMAIL_DEFAULT_FROM_EMAIL", default=BULK_EMAIL_DEFAULT_FROM_EMAIL
)
BULK_EMAIL_EMAILS_PER_TASK = config(
    "BULK_EMAIL_EMAILS_PER_TASK", default=BULK_EMAIL_EMAILS_PER_TASK, formatter=int
)
BULK_EMAIL_DEFAULT_RETRY_DELAY = config(
    "BULK_EMAIL_DEFAULT_RETRY_DELAY",
    default=BULK_EMAIL_DEFAULT_RETRY_DELAY,
    formatter=int,
)
BULK_EMAIL_MAX_RETRIES = config(
    "BULK_EMAIL_MAX_RETRIES", default=BULK_EMAIL_MAX_RETRIES, formatter=int
)
BULK_EMAIL_INFINITE_RETRY_CAP = config(
    "BULK_EMAIL_INFINITE_RETRY_CAP",
    default=BULK_EMAIL_INFINITE_RETRY_CAP,
    formatter=int,
)
BULK_EMAIL_LOG_SENT_EMAILS = config(
    "BULK_EMAIL_LOG_SENT_EMAILS", default=BULK_EMAIL_LOG_SENT_EMAILS, formatter=bool
)
BULK_EMAIL_RETRY_DELAY_BETWEEN_SENDS = config(
    "BULK_EMAIL_RETRY_DELAY_BETWEEN_SENDS",
    default=BULK_EMAIL_RETRY_DELAY_BETWEEN_SENDS,
    formatter=int,
)
# We want Bulk Email running on the high-priority queue, so we define the
# routing key that points to it. At the moment, the name is the same.
# We have to reset the value here, since we have changed the value of the queue name.
BULK_EMAIL_ROUTING_KEY = config("BULK_EMAIL_ROUTING_KEY", default=HIGH_PRIORITY_QUEUE)

# We can run smaller jobs on the low priority queue. See note above for why
# we have to reset the value here.
BULK_EMAIL_ROUTING_KEY_SMALL_JOBS = config(
    "BULK_EMAIL_ROUTING_KEY_SMALL_JOBS", default=LOW_PRIORITY_QUEUE
)

# Queue to use for expiring old entitlements
ENTITLEMENTS_EXPIRATION_ROUTING_KEY = config(
    "ENTITLEMENTS_EXPIRATION_ROUTING_KEY", default=LOW_PRIORITY_QUEUE
)

# Message expiry time in seconds
CELERY_EVENT_QUEUE_TTL = config("CELERY_EVENT_QUEUE_TTL", default=None, formatter=int)

# following setting is for backward compatibility
if config("COMPREHENSIVE_THEME_DIR", default=None):
    COMPREHENSIVE_THEME_DIR = config("COMPREHENSIVE_THEME_DIR")

COMPREHENSIVE_THEME_DIRS = (
    config(
        "COMPREHENSIVE_THEME_DIRS",
        default=COMPREHENSIVE_THEME_DIRS,
        formatter=json.loads,
    )
    or []
)

LOCALE_PATHS = config(
    "LOCALE_PATHS", default=(REPO_ROOT + "/conf/locale",), formatter=json.loads
)

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

# Marketing link overrides
MKTG_URL_LINK_MAP = config("MKTG_URL_LINK_MAP", default={}, formatter=json.loads)

# Intentional defaults.
SUPPORT_SITE_LINK = config("SUPPORT_SITE_LINK", default=SUPPORT_SITE_LINK)
ID_VERIFICATION_SUPPORT_LINK = config(
    "ID_VERIFICATION_SUPPORT_LINK", default=SUPPORT_SITE_LINK
)
PASSWORD_RESET_SUPPORT_LINK = config(
    "PASSWORD_RESET_SUPPORT_LINK", default=SUPPORT_SITE_LINK
)
ACTIVATION_EMAIL_SUPPORT_LINK = config(
    "ACTIVATION_EMAIL_SUPPORT_LINK", default=SUPPORT_SITE_LINK
)

# Mobile store URL overrides
MOBILE_STORE_URLS = config(
    "MOBILE_STORE_URLS", default=MOBILE_STORE_URLS, formatter=json.loads
)

# Timezone overrides
TIME_ZONE = config("TIME_ZONE", default=TIME_ZONE)

# Translation overrides
LANGUAGES = config("LANGUAGES", default=LANGUAGES, formatter=json.loads)
CERTIFICATE_TEMPLATE_LANGUAGES = config(
    "CERTIFICATE_TEMPLATE_LANGUAGES",
    default=CERTIFICATE_TEMPLATE_LANGUAGES,
    formatter=json.loads,
)
LANGUAGE_DICT = dict(LANGUAGES)
LANGUAGE_CODE = config("LANGUAGE_CODE", default=LANGUAGE_CODE)
LANGUAGE_COOKIE = config("LANGUAGE_COOKIE", default=LANGUAGE_COOKIE)
ALL_LANGUAGES = config("ALL_LANGUAGES", default=ALL_LANGUAGES, formatter=json.loads)

USE_I18N = config("USE_I18N", default=USE_I18N, formatter=bool)

# Additional installed apps
for app in config("ADDL_INSTALLED_APPS", default=[], formatter=json.loads):
    INSTALLED_APPS.append(app)

WIKI_ENABLED = config("WIKI_ENABLED", default=WIKI_ENABLED, formatter=bool)
local_loglevel = config("LOCAL_LOGLEVEL", default="INFO")

# Default format for syslog logging
standard_format = "%(asctime)s %(levelname)s %(process)d [%(name)s] %(filename)s:%(lineno)d - %(message)s"
syslog_format = (
    "[variant:lms][%(name)s][env:sandbox] %(levelname)s "
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


COURSE_LISTINGS = config("COURSE_LISTINGS", default={}, formatter=json.loads)
COMMENTS_SERVICE_URL = config("COMMENTS_SERVICE_URL", default="")
COMMENTS_SERVICE_KEY = config("COMMENTS_SERVICE_KEY", default="")
CERT_NAME_SHORT = config("CERT_NAME_SHORT", default=CERT_NAME_SHORT)
CERT_NAME_LONG = config("CERT_NAME_LONG", default=CERT_NAME_LONG)
CERT_QUEUE = config("CERT_QUEUE", default="test-pull")

FEEDBACK_SUBMISSION_EMAIL = config("FEEDBACK_SUBMISSION_EMAIL", default=None)
MKTG_URLS = config("MKTG_URLS", default=MKTG_URLS, formatter=json.loads)

# Badgr API
BADGR_API_TOKEN = config("BADGR_API_TOKEN", default=BADGR_API_TOKEN)
BADGR_BASE_URL = config("BADGR_BASE_URL", default=BADGR_BASE_URL)
BADGR_ISSUER_SLUG = config("BADGR_ISSUER_SLUG", default=BADGR_ISSUER_SLUG)
BADGR_TIMEOUT = config("BADGR_TIMEOUT", default=BADGR_TIMEOUT, formatter=int)

# git repo loading  environment
GIT_REPO_DIR = config(
    "GIT_REPO_DIR", default=path("/edx/var/edxapp/course_repos"), formatter=path
)
GIT_IMPORT_STATIC = config("GIT_IMPORT_STATIC", default=True, formatter=bool)
GIT_IMPORT_PYTHON_LIB = config("GIT_IMPORT_PYTHON_LIB", default=True, formatter=bool)
PYTHON_LIB_FILENAME = config("PYTHON_LIB_FILENAME", default="python_lib.zip")

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

# Event Tracking
TRACKING_IGNORE_URL_PATTERNS = config(
    "TRACKING_IGNORE_URL_PATTERNS",
    default=TRACKING_IGNORE_URL_PATTERNS,
    formatter=json.loads,
)

# SSL external authentication settings
SSL_AUTH_EMAIL_DOMAIN = config("SSL_AUTH_EMAIL_DOMAIN", default="MIT.EDU")
SSL_AUTH_DN_FORMAT_STRING = config("SSL_AUTH_DN_FORMAT_STRING", default=None)

# Django CAS external authentication settings
CAS_EXTRA_LOGIN_PARAMS = config(
    "CAS_EXTRA_LOGIN_PARAMS", default=None, formatter=json.loads
)
if FEATURES.get("AUTH_USE_CAS"):
    CAS_SERVER_URL = config("CAS_SERVER_URL", default=None)
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

# Video Caching. Pairing country codes with CDN URLs.
# Example: {'CN': 'http://api.xuetangx.com/edx/video?s3_url='}
VIDEO_CDN_URL = config("VIDEO_CDN_URL", default={})

# Branded footer
FOOTER_OPENEDX_URL = config("FOOTER_OPENEDX_URL", default=FOOTER_OPENEDX_URL)
FOOTER_OPENEDX_LOGO_IMAGE = config(
    "FOOTER_OPENEDX_LOGO_IMAGE", default=FOOTER_OPENEDX_LOGO_IMAGE
)
FOOTER_ORGANIZATION_IMAGE = config(
    "FOOTER_ORGANIZATION_IMAGE", default=FOOTER_ORGANIZATION_IMAGE
)
FOOTER_CACHE_TIMEOUT = config(
    "FOOTER_CACHE_TIMEOUT", default=FOOTER_CACHE_TIMEOUT, formatter=int
)
FOOTER_BROWSER_CACHE_MAX_AGE = config(
    "FOOTER_BROWSER_CACHE_MAX_AGE", default=FOOTER_BROWSER_CACHE_MAX_AGE, formatter=int
)

# Credit notifications settings
NOTIFICATION_EMAIL_CSS = config(
    "NOTIFICATION_EMAIL_CSS", default=NOTIFICATION_EMAIL_CSS
)
NOTIFICATION_EMAIL_EDX_LOGO = config(
    "NOTIFICATION_EMAIL_EDX_LOGO", default=NOTIFICATION_EMAIL_EDX_LOGO
)
SECRET_KEY = config("SECRET_KEY", default="ThisIsAnExampleKeyForDevPurposeOnly")

# Authentication backends
# - behind a proxy, use: "lms.envs.fun.backends.ProxyRateLimitModelBackend"
# - for LTI provider, add: "lti_provider.users.LtiBackend"
# - for CAS, add: "django_cas.backends.CASBackend"
AUTHENTICATION_BACKENDS = config(
    "AUTHENTICATION_BACKENDS",
    default=("lms.envs.fun.backends.ProxyRateLimitModelBackend",),
)

# Determines whether the CSRF token can be transported on
# unencrypted channels. It is set to False here for backward compatibility,
# but it is highly recommended that this is True for enviroments accessed
# by end users.
CSRF_COOKIE_SECURE = config("CSRF_COOKIE_SECURE", default=False, formatter=bool)

############# CORS headers for cross-domain requests #################

if FEATURES.get("ENABLE_CORS_HEADERS") or FEATURES.get(
    "ENABLE_CROSS_DOMAIN_CSRF_COOKIE"
):
    CORS_ALLOW_CREDENTIALS = True
    CORS_ORIGIN_WHITELIST = config(
        "CORS_ORIGIN_WHITELIST", default=(), formatter=json.loads
    )
    CORS_ORIGIN_ALLOW_ALL = config(
        "CORS_ORIGIN_ALLOW_ALL", default=False, formatter=bool
    )
    CORS_ALLOW_INSECURE = config("CORS_ALLOW_INSECURE", default=False, formatter=bool)

    # If setting a cross-domain cookie, it's really important to choose
    # a name for the cookie that is DIFFERENT than the cookies used
    # by each subdomain.  For example, suppose the applications
    # at these subdomains are configured to use the following cookie names:
    #
    # 1) foo.example.com --> "csrftoken"
    # 2) baz.example.com --> "csrftoken"
    # 3) bar.example.com --> "csrftoken"
    #
    # For the cross-domain version of the CSRF cookie, you need to choose
    # a name DIFFERENT than "csrftoken"; otherwise, the new token configured
    # for ".example.com" could conflict with the other cookies,
    # non-deterministically causing 403 responses.
    #
    # Because of the way Django stores cookies, the cookie name MUST
    # be a `str`, not unicode.  Otherwise there will `TypeError`s will be raised
    # when Django tries to call the unicode `translate()` method with the wrong
    # number of parameters.
    CROSS_DOMAIN_CSRF_COOKIE_NAME = str(config("CROSS_DOMAIN_CSRF_COOKIE_NAME"))

    # When setting the domain for the "cross-domain" version of the CSRF
    # cookie, you should choose something like: ".example.com"
    # (note the leading dot), where both the referer and the host
    # are subdomains of "example.com".
    #
    # Browser security rules require that
    # the cookie domain matches the domain of the server; otherwise
    # the cookie won't get set.  And once the cookie gets set, the client
    # needs to be on a domain that matches the cookie domain, otherwise
    # the client won't be able to read the cookie.
    CROSS_DOMAIN_CSRF_COOKIE_DOMAIN = config("CROSS_DOMAIN_CSRF_COOKIE_DOMAIN")


# Field overrides. To use the IDDE feature, add
# 'courseware.student_field_overrides.IndividualStudentOverrideProvider'.
FIELD_OVERRIDE_PROVIDERS = tuple(
    config("FIELD_OVERRIDE_PROVIDERS", default=[], formatter=json.loads)
)

############################## SECURE AUTH ITEMS ###############

############### XBlock filesystem field config ##########
DJFS = config("DJFS", default=None, formatter=json.loads)

############### Module Store Items ##########
HOSTNAME_MODULESTORE_DEFAULT_MAPPINGS = config(
    "HOSTNAME_MODULESTORE_DEFAULT_MAPPINGS", default={}, formatter=json.loads
)
# PREVIEW DOMAIN must be present in HOSTNAME_MODULESTORE_DEFAULT_MAPPINGS for the preview to show
# draft changes
if "PREVIEW_LMS_BASE" in FEATURES and FEATURES["PREVIEW_LMS_BASE"] != "":
    PREVIEW_DOMAIN = FEATURES["PREVIEW_LMS_BASE"].split(":")[0]
    # update dictionary with preview domain regex
    HOSTNAME_MODULESTORE_DEFAULT_MAPPINGS.update({PREVIEW_DOMAIN: "draft-preferred"})

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

############### Mixed Related(Secure/Not-Secure) Items ##########
LMS_SEGMENT_KEY = config("LMS_SEGMENT_KEY", default=None)

CC_PROCESSOR_NAME = config("CC_PROCESSOR_NAME", default=CC_PROCESSOR_NAME)
CC_PROCESSOR = config("CC_PROCESSOR", default=CC_PROCESSOR, formatter=json.loads)


DEFAULT_FILE_STORAGE = config(
    "DEFAULT_FILE_STORAGE", default="django.core.files.storage.FileSystemStorage"
)

# Specific setting for the File Upload Service to store media in a bucket.
FILE_UPLOAD_STORAGE_BUCKET_NAME = config(
    "FILE_UPLOAD_STORAGE_BUCKET_NAME", default="uploads"
)
FILE_UPLOAD_STORAGE_PREFIX = config(
    "FILE_UPLOAD_STORAGE_PREFIX", default=FILE_UPLOAD_STORAGE_PREFIX
)

# Databases

# If there is a database called 'read_replica', you can use the use_read_replica_if_available
# function in util/query.py, which is useful for very large database reads

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

XQUEUE_INTERFACE = config(
    "XQUEUE_INTERFACE",
    default={"url": None, "basic_auth": None, "django_auth": None},
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

MONGODB_LOG = config("MONGODB_LOG", default={}, formatter=json.loads)

CONTENTSTORE = config(
    "CONTENTSTORE",
    default={
        "DOC_STORE_CONFIG": DOC_STORE_CONFIG,
        "ENGINE": "xmodule.contentstore.mongo.MongoContentStore",
    },
    formatter=json.loads,
)

update_module_store_settings(MODULESTORE, doc_store_settings=DOC_STORE_CONFIG)

EMAIL_HOST_USER = config("EMAIL_HOST_USER", default="")  # django default is ''
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD", default="")  # django default is ''

# Datadog for events!
DATADOG = config("DATADOG", default={}, formatter=json.loads)

# TODO: deprecated (compatibility with previous settings)
DATADOG_API = config("DATADOG_API", default=None)

# Analytics API
ANALYTICS_API_KEY = config("ANALYTICS_API_KEY", default=ANALYTICS_API_KEY)
ANALYTICS_API_URL = config("ANALYTICS_API_URL", default=ANALYTICS_API_URL)

# Mailchimp New User List
MAILCHIMP_NEW_USER_LIST_ID = config("MAILCHIMP_NEW_USER_LIST_ID", default=None)

# Zendesk
ZENDESK_URL = config("ZENDESK_URL", default=None)
ZENDESK_USER = config("ZENDESK_USER", default=None)
ZENDESK_API_KEY = config("ZENDESK_API_KEY", default=None)
ZENDESK_CUSTOM_FIELDS = config(
    "ZENDESK_CUSTOM_FIELDS", default={}, formatter=json.loads
)

# API Key for inbound requests from Notifier service
EDX_API_KEY = config("EDX_API_KEY", default=None)

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

# Block Structures
BLOCK_STRUCTURES_SETTINGS = config(
    "BLOCK_STRUCTURES_SETTINGS", default=BLOCK_STRUCTURES_SETTINGS, formatter=json.loads
)

# upload limits
STUDENT_FILEUPLOAD_MAX_SIZE = config(
    "STUDENT_FILEUPLOAD_MAX_SIZE", default=STUDENT_FILEUPLOAD_MAX_SIZE, formatter=int
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
TRACKING_SEGMENTIO_WEBHOOK_SECRET = config(
    "TRACKING_SEGMENTIO_WEBHOOK_SECRET", default=TRACKING_SEGMENTIO_WEBHOOK_SECRET
)
TRACKING_SEGMENTIO_ALLOWED_TYPES = config(
    "TRACKING_SEGMENTIO_ALLOWED_TYPES",
    default=TRACKING_SEGMENTIO_ALLOWED_TYPES,
    formatter=json.loads,
)
TRACKING_SEGMENTIO_DISALLOWED_SUBSTRING_NAMES = config(
    "TRACKING_SEGMENTIO_DISALLOWED_SUBSTRING_NAMES",
    default=TRACKING_SEGMENTIO_DISALLOWED_SUBSTRING_NAMES,
    formatter=json.loads,
)
TRACKING_SEGMENTIO_SOURCE_MAP = config(
    "TRACKING_SEGMENTIO_SOURCE_MAP",
    default=TRACKING_SEGMENTIO_SOURCE_MAP,
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

# Student identity verification settings
VERIFY_STUDENT = config("VERIFY_STUDENT", default=VERIFY_STUDENT, formatter=json.loads)
DISABLE_ACCOUNT_ACTIVATION_REQUIREMENT_SWITCH = config(
    "DISABLE_ACCOUNT_ACTIVATION_REQUIREMENT_SWITCH",
    default=DISABLE_ACCOUNT_ACTIVATION_REQUIREMENT_SWITCH,
)

# Grades download
GRADES_DOWNLOAD_ROUTING_KEY = config(
    "GRADES_DOWNLOAD_ROUTING_KEY", default=HIGH_MEM_QUEUE
)

# Fonzie API endpoint to add access control on instructor dashboard
# CSV export files (activated by features ENABLE_GRADE_DOWNLOADS and
# ALLOW_COURSE_STAFF_GRADE_DOWNLOADS)
GRADES_DOWNLOAD = config(
    "GRADES_DOWNLOAD",
    default={
        "STORAGE_CLASS": "django.core.files.storage.FileSystemStorage",
        "STORAGE_KWARGS": {
            "location": "/edx/var/edxapp/export",
            "base_url": "/api/v1.0/acl/report",
        },
    },
    formatter=json.loads,
)

# Add Django Rest Framework URL versioning required by Fonzie to edX
# existing DRF configuration
REST_FRAMEWORK.update(
    {
        "ALLOWED_VERSIONS": ("1.0",),
        "DEFAULT_VERSION": "1.0",
        "DEFAULT_VERSIONING_CLASS": "rest_framework.versioning.URLPathVersioning",
    }
)

# Rate limit for regrading tasks that a grading policy change can kick off
POLICY_CHANGE_TASK_RATE_LIMIT = config(
    "POLICY_CHANGE_TASK_RATE_LIMIT", default=POLICY_CHANGE_TASK_RATE_LIMIT
)

# financial reports
FINANCIAL_REPORTS = config(
    "FINANCIAL_REPORTS", default=FINANCIAL_REPORTS, formatter=json.loads
)

##### ORA2 ######
ORA2_FILEUPLOAD_BACKEND = config("ORA2_FILEUPLOAD_BACKEND", default="filesystem")

# Prefix for uploads of example-based assessment AI classifiers
# This can be used to separate uploads for different environments
ORA2_FILE_PREFIX = config("ORA2_FILE_PREFIX", default=ORA2_FILE_PREFIX)

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

##### LMS DEADLINE DISPLAY TIME_ZONE #######
TIME_ZONE_DISPLAYED_FOR_DEADLINES = config(
    "TIME_ZONE_DISPLAYED_FOR_DEADLINES", default=TIME_ZONE_DISPLAYED_FOR_DEADLINES
)

##### X-Frame-Options response header settings #####
X_FRAME_OPTIONS = config("X_FRAME_OPTIONS", default=X_FRAME_OPTIONS)

##### Third-party auth options ################################################
if FEATURES.get("ENABLE_THIRD_PARTY_AUTH"):
    # The reduced session expiry time during the third party login pipeline. (Value in seconds)
    SOCIAL_AUTH_PIPELINE_TIMEOUT = config(
        "SOCIAL_AUTH_PIPELINE_TIMEOUT", default=600, formatter=int
    )

    # The SAML private/public key values do not need the delimiter lines (such as
    # "-----BEGIN PRIVATE KEY-----", "-----END PRIVATE KEY-----" etc.) but they may be included
    # if you want (though it's easier to format the key values as JSON without the delimiters).
    SOCIAL_AUTH_SAML_SP_PRIVATE_KEY = config(
        "SOCIAL_AUTH_SAML_SP_PRIVATE_KEY", default={}, formatter=json.loads
    )
    SOCIAL_AUTH_SAML_SP_PUBLIC_CERT = config(
        "SOCIAL_AUTH_SAML_SP_PUBLIC_CERT", default={}, formatter=json.loads
    )
    SOCIAL_AUTH_OAUTH_SECRETS = config("SOCIAL_AUTH_OAUTH_SECRETS", default={})
    SOCIAL_AUTH_LTI_CONSUMER_SECRETS = config(
        "SOCIAL_AUTH_LTI_CONSUMER_SECRETS", default={}, formatter=json.loads
    )

    # third_party_auth config moved to ConfigurationModels. This is for data migration only:
    THIRD_PARTY_AUTH_OLD_CONFIG = config("THIRD_PARTY_AUTH", default=None)

    if (
        config("THIRD_PARTY_AUTH_SAML_FETCH_PERIOD_HOURS", default=24, formatter=int)
        is not None
    ):
        CELERYBEAT_SCHEDULE["refresh-saml-metadata"] = {
            "task": "third_party_auth.fetch_saml_metadata",
            "schedule": datetime.timedelta(
                hours=config(
                    "THIRD_PARTY_AUTH_SAML_FETCH_PERIOD_HOURS",
                    default=24,
                    formatter=int,
                )
            ),
        }

    # The following can be used to integrate a custom login form with third_party_auth.
    # It should be a dict where the key is a word passed via ?auth_entry=, and the value is a
    # dict with an arbitrary 'secret_key' and a 'url'.
    THIRD_PARTY_AUTH_CUSTOM_AUTH_FORMS = config(
        "THIRD_PARTY_AUTH_CUSTOM_AUTH_FORMS", default={}, formatter=json.loads
    )

##### OAUTH2 Provider ##############
if FEATURES.get("ENABLE_OAUTH2_PROVIDER"):
    OAUTH_OIDC_ISSUER = config("OAUTH_OIDC_ISSUER")
    OAUTH_ENFORCE_SECURE = config("OAUTH_ENFORCE_SECURE", default=True, formatter=bool)
    OAUTH_ENFORCE_CLIENT_SECURE = config(
        "OAUTH_ENFORCE_CLIENT_SECURE", default=True, formatter=bool
    )
    # Defaults for the following are defined in lms.envs.common
    OAUTH_EXPIRE_DELTA = datetime.timedelta(
        days=config(
            "OAUTH_EXPIRE_CONFIDENTIAL_CLIENT_DAYS",
            default=OAUTH_EXPIRE_CONFIDENTIAL_CLIENT_DAYS,
            formatter=int,
        )
    )
    OAUTH_EXPIRE_DELTA_PUBLIC = datetime.timedelta(
        days=config(
            "OAUTH_EXPIRE_PUBLIC_CLIENT_DAYS",
            default=OAUTH_EXPIRE_PUBLIC_CLIENT_DAYS,
            formatter=int,
        )
    )
    OAUTH_ID_TOKEN_EXPIRATION = config(
        "OAUTH_ID_TOKEN_EXPIRATION", default=OAUTH_ID_TOKEN_EXPIRATION, formatter=int
    )
    OAUTH_DELETE_EXPIRED = config(
        "OAUTH_DELETE_EXPIRED", default=OAUTH_DELETE_EXPIRED, formatter=bool
    )

##### ADVANCED_SECURITY_CONFIG #####
ADVANCED_SECURITY_CONFIG = config(
    "ADVANCED_SECURITY_CONFIG", default={}, formatter=json.loads
)

##### GOOGLE ANALYTICS IDS #####
GOOGLE_ANALYTICS_ACCOUNT = config("GOOGLE_ANALYTICS_ACCOUNT", default=None)
GOOGLE_ANALYTICS_TRACKING_ID = config("GOOGLE_ANALYTICS_TRACKING_ID", default=None)
GOOGLE_ANALYTICS_LINKEDIN = config("GOOGLE_ANALYTICS_LINKEDIN", default=None)
GOOGLE_SITE_VERIFICATION_ID = config("GOOGLE_SITE_VERIFICATION_ID", default=None)

##### BRANCH.IO KEY #####
BRANCH_IO_KEY = config("BRANCH_IO_KEY", default=None)

##### OPTIMIZELY PROJECT ID #####
OPTIMIZELY_PROJECT_ID = config("OPTIMIZELY_PROJECT_ID", default=OPTIMIZELY_PROJECT_ID)

#### Course Registration Code length ####
REGISTRATION_CODE_LENGTH = config("REGISTRATION_CODE_LENGTH", default=8, formatter=int)

# REGISTRATION CODES DISPLAY INFORMATION
INVOICE_CORP_ADDRESS = config("INVOICE_CORP_ADDRESS", default=INVOICE_CORP_ADDRESS)
INVOICE_PAYMENT_INSTRUCTIONS = config(
    "INVOICE_PAYMENT_INSTRUCTIONS", default=INVOICE_PAYMENT_INSTRUCTIONS
)

# Which access.py permission names to check;
# We default this to the legacy permission 'see_exists'.
COURSE_CATALOG_VISIBILITY_PERMISSION = config(
    "COURSE_CATALOG_VISIBILITY_PERMISSION", default=COURSE_CATALOG_VISIBILITY_PERMISSION
)
COURSE_ABOUT_VISIBILITY_PERMISSION = config(
    "COURSE_ABOUT_VISIBILITY_PERMISSION", default=COURSE_ABOUT_VISIBILITY_PERMISSION
)

DEFAULT_COURSE_VISIBILITY_IN_CATALOG = config(
    "DEFAULT_COURSE_VISIBILITY_IN_CATALOG", default=DEFAULT_COURSE_VISIBILITY_IN_CATALOG
)

DEFAULT_MOBILE_AVAILABLE = config(
    "DEFAULT_MOBILE_AVAILABLE", default=DEFAULT_MOBILE_AVAILABLE, formatter=bool
)

# Enrollment API Cache Timeout
ENROLLMENT_COURSE_DETAILS_CACHE_TIMEOUT = config(
    "ENROLLMENT_COURSE_DETAILS_CACHE_TIMEOUT", default=60, formatter=int
)

# PDF RECEIPT/INVOICE OVERRIDES
PDF_RECEIPT_TAX_ID = config("PDF_RECEIPT_TAX_ID", default=PDF_RECEIPT_TAX_ID)
PDF_RECEIPT_FOOTER_TEXT = config(
    "PDF_RECEIPT_FOOTER_TEXT", default=PDF_RECEIPT_FOOTER_TEXT
)
PDF_RECEIPT_DISCLAIMER_TEXT = config(
    "PDF_RECEIPT_DISCLAIMER_TEXT", default=PDF_RECEIPT_DISCLAIMER_TEXT
)
PDF_RECEIPT_BILLING_ADDRESS = config(
    "PDF_RECEIPT_BILLING_ADDRESS", default=PDF_RECEIPT_BILLING_ADDRESS
)
PDF_RECEIPT_TERMS_AND_CONDITIONS = config(
    "PDF_RECEIPT_TERMS_AND_CONDITIONS", default=PDF_RECEIPT_TERMS_AND_CONDITIONS
)
PDF_RECEIPT_TAX_ID_LABEL = config(
    "PDF_RECEIPT_TAX_ID_LABEL", default=PDF_RECEIPT_TAX_ID_LABEL
)
PDF_RECEIPT_LOGO_PATH = config("PDF_RECEIPT_LOGO_PATH", default=PDF_RECEIPT_LOGO_PATH)
PDF_RECEIPT_COBRAND_LOGO_PATH = config(
    "PDF_RECEIPT_COBRAND_LOGO_PATH", default=PDF_RECEIPT_COBRAND_LOGO_PATH
)
PDF_RECEIPT_LOGO_HEIGHT_MM = config(
    "PDF_RECEIPT_LOGO_HEIGHT_MM", default=PDF_RECEIPT_LOGO_HEIGHT_MM, formatter=int
)
PDF_RECEIPT_COBRAND_LOGO_HEIGHT_MM = config(
    "PDF_RECEIPT_COBRAND_LOGO_HEIGHT_MM",
    default=PDF_RECEIPT_COBRAND_LOGO_HEIGHT_MM,
    formatter=int,
)

if (
    FEATURES.get("ENABLE_COURSEWARE_SEARCH")
    or FEATURES.get("ENABLE_DASHBOARD_SEARCH")
    or FEATURES.get("ENABLE_COURSE_DISCOVERY")
    or FEATURES.get("ENABLE_TEAMS")
):
    # Use ElasticSearch as the search engine herein
    SEARCH_ENGINE = "search.elastic.ElasticSearchEngine"

ELASTIC_SEARCH_CONFIG = config(
    "ELASTIC_SEARCH_CONFIG", default=[{}], formatter=json.loads
)

# Facebook app
FACEBOOK_API_VERSION = config("FACEBOOK_API_VERSION", default=None)
FACEBOOK_APP_SECRET = config(
    "FACEBOOK_APP_SECRET", default="ThisIsAnExampleKeyForDevPurposeOnly"
)
FACEBOOK_APP_ID = config("FACEBOOK_APP_ID", default=None)

XBLOCK_SETTINGS = config("XBLOCK_SETTINGS", default={}, formatter=json.loads)
XBLOCK_SETTINGS.setdefault("VideoDescriptor", {})["licensing_enabled"] = FEATURES.get(
    "LICENSING", False
)
XBLOCK_SETTINGS.setdefault("VideoModule", {})["YOUTUBE_API_KEY"] = config(
    "YOUTUBE_API_KEY", default=YOUTUBE_API_KEY
)

##### VIDEO IMAGE STORAGE #####
VIDEO_IMAGE_SETTINGS = config(
    "VIDEO_IMAGE_SETTINGS", default=VIDEO_IMAGE_SETTINGS, formatter=json.loads
)

##### VIDEO TRANSCRIPTS STORAGE #####
VIDEO_TRANSCRIPTS_SETTINGS = config(
    "VIDEO_TRANSCRIPTS_SETTINGS",
    default=VIDEO_TRANSCRIPTS_SETTINGS,
    formatter=json.loads,
)

##### ECOMMERCE API CONFIGURATION SETTINGS #####
ECOMMERCE_PUBLIC_URL_ROOT = config(
    "ECOMMERCE_PUBLIC_URL_ROOT", default=ECOMMERCE_PUBLIC_URL_ROOT
)
ECOMMERCE_API_URL = config("ECOMMERCE_API_URL", default=ECOMMERCE_API_URL)
ECOMMERCE_API_TIMEOUT = config(
    "ECOMMERCE_API_TIMEOUT", default=ECOMMERCE_API_TIMEOUT, formatter=int
)

COURSE_CATALOG_API_URL = config(
    "COURSE_CATALOG_API_URL", default=COURSE_CATALOG_API_URL
)

ECOMMERCE_SERVICE_WORKER_USERNAME = config(
    "ECOMMERCE_SERVICE_WORKER_USERNAME", default=ECOMMERCE_SERVICE_WORKER_USERNAME
)

##### Custom Courses for EdX #####
if FEATURES.get("CUSTOM_COURSES_EDX"):
    INSTALLED_APPS += [
        "lms.djangoapps.ccx",
        "openedx.core.djangoapps.ccxcon.apps.CCXConnectorConfig",
    ]
    MODULESTORE_FIELD_OVERRIDE_PROVIDERS += (
        "lms.djangoapps.ccx.overrides.CustomCoursesForEdxOverrideProvider",
    )
CCX_MAX_STUDENTS_ALLOWED = config(
    "CCX_MAX_STUDENTS_ALLOWED", default=CCX_MAX_STUDENTS_ALLOWED, formatter=int
)

##### Individual Due Date Extensions #####
if FEATURES.get("INDIVIDUAL_DUE_DATES"):
    FIELD_OVERRIDE_PROVIDERS += (
        "courseware.student_field_overrides.IndividualStudentOverrideProvider",
    )

##### Self-Paced Course Due Dates #####
XBLOCK_FIELD_DATA_WRAPPERS += (
    "lms.djangoapps.courseware.field_overrides:OverrideModulestoreFieldData.wrap",
)

MODULESTORE_FIELD_OVERRIDE_PROVIDERS += (
    "courseware.self_paced_overrides.SelfPacedDateOverrideProvider",
)

# PROFILE IMAGE CONFIG
PROFILE_IMAGE_BACKEND = config("PROFILE_IMAGE_BACKEND", default=PROFILE_IMAGE_BACKEND)
PROFILE_IMAGE_SECRET_KEY = config(
    "PROFILE_IMAGE_SECRET_KEY", default=PROFILE_IMAGE_SECRET_KEY
)
PROFILE_IMAGE_MAX_BYTES = config(
    "PROFILE_IMAGE_MAX_BYTES", default=PROFILE_IMAGE_MAX_BYTES, formatter=int
)
PROFILE_IMAGE_MIN_BYTES = config(
    "PROFILE_IMAGE_MIN_BYTES", default=PROFILE_IMAGE_MIN_BYTES, formatter=int
)
PROFILE_IMAGE_DEFAULT_FILENAME = "images/profiles/default"
PROFILE_IMAGE_SIZES_MAP = config(
    "PROFILE_IMAGE_SIZES_MAP", default=PROFILE_IMAGE_SIZES_MAP, formatter=json.loads
)

# EdxNotes config

EDXNOTES_PUBLIC_API = config("EDXNOTES_PUBLIC_API", default=EDXNOTES_PUBLIC_API)
EDXNOTES_INTERNAL_API = config("EDXNOTES_INTERNAL_API", default=EDXNOTES_INTERNAL_API)

EDXNOTES_CONNECT_TIMEOUT = config(
    "EDXNOTES_CONNECT_TIMEOUT", default=EDXNOTES_CONNECT_TIMEOUT, formatter=int
)
EDXNOTES_READ_TIMEOUT = config(
    "EDXNOTES_READ_TIMEOUT", default=EDXNOTES_READ_TIMEOUT, formatter=int
)

##### Credit Provider Integration #####

CREDIT_PROVIDER_SECRET_KEYS = config(
    "CREDIT_PROVIDER_SECRET_KEYS", default={}, formatter=json.loads
)

##################### LTI Provider #####################
if FEATURES.get("ENABLE_LTI_PROVIDER"):
    INSTALLED_APPS.append("lti_provider.apps.LtiProviderConfig")

LTI_USER_EMAIL_DOMAIN = config("LTI_USER_EMAIL_DOMAIN", default="lti.example.com")

# For more info on this, see the notes in common.py
LTI_AGGREGATE_SCORE_PASSBACK_DELAY = config(
    "LTI_AGGREGATE_SCORE_PASSBACK_DELAY",
    default=LTI_AGGREGATE_SCORE_PASSBACK_DELAY,
    formatter=int,
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

##################### Credit Provider help link ####################
CREDIT_HELP_LINK_URL = config("CREDIT_HELP_LINK_URL", default=CREDIT_HELP_LINK_URL)

#### JWT configuration ####
DEFAULT_JWT_ISSUER = config("DEFAULT_JWT_ISSUER", default=DEFAULT_JWT_ISSUER)
RESTRICTED_APPLICATION_JWT_ISSUER = config(
    "RESTRICTED_APPLICATION_JWT_ISSUER", default=RESTRICTED_APPLICATION_JWT_ISSUER
)
JWT_AUTH.update(config("JWT_AUTH", default={}, formatter=json.loads))
JWT_PRIVATE_SIGNING_KEY = config(
    "JWT_PRIVATE_SIGNING_KEY", default=JWT_PRIVATE_SIGNING_KEY
)
JWT_EXPIRED_PRIVATE_SIGNING_KEYS = config(
    "JWT_EXPIRED_PRIVATE_SIGNING_KEYS",
    default=JWT_EXPIRED_PRIVATE_SIGNING_KEYS,
    formatter=json.loads,
)

################# PROCTORING CONFIGURATION ##################

PROCTORING_BACKEND_PROVIDER = config(
    "PROCTORING_BACKEND_PROVIDER", default=PROCTORING_BACKEND_PROVIDER
)
PROCTORING_SETTINGS = config(
    "PROCTORING_SETTINGS", default=PROCTORING_SETTINGS, formatter=json.loads
)

################# MICROSITE ####################
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

# Offset for pk of courseware.StudentModuleHistoryExtended
STUDENTMODULEHISTORYEXTENDED_OFFSET = config(
    "STUDENTMODULEHISTORYEXTENDED_OFFSET",
    default=STUDENTMODULEHISTORYEXTENDED_OFFSET,
    formatter=int,
)

# Cutoff date for granting audit certificates
AUDIT_CERT_CUTOFF_DATE = config(
    "AUDIT_CERT_CUTOFF_DATE", default=None, formatter=dateutil.parser.parse
)

################################ Settings for Credentials Service ################################

CREDENTIALS_GENERATION_ROUTING_KEY = config(
    "CREDENTIALS_GENERATION_ROUTING_KEY", default=HIGH_PRIORITY_QUEUE
)

# The extended StudentModule history table
if FEATURES.get("ENABLE_CSMH_EXTENDED"):
    INSTALLED_APPS.append("coursewarehistoryextended")

API_ACCESS_MANAGER_EMAIL = config(
    "API_ACCESS_MANAGER_EMAIL", default=API_ACCESS_MANAGER_EMAIL
)
API_ACCESS_FROM_EMAIL = config("API_ACCESS_FROM_EMAIL", default=API_ACCESS_FROM_EMAIL)

# Mobile App Version Upgrade config
APP_UPGRADE_CACHE_TIMEOUT = config(
    "APP_UPGRADE_CACHE_TIMEOUT", default=APP_UPGRADE_CACHE_TIMEOUT, formatter=int
)

AFFILIATE_COOKIE_NAME = config("AFFILIATE_COOKIE_NAME", default=AFFILIATE_COOKIE_NAME)

############## Settings for LMS Context Sensitive Help ##############

HELP_TOKENS_BOOKS = config(
    "HELP_TOKENS_BOOKS", default=HELP_TOKENS_BOOKS, formatter=json.loads
)


############## OPEN EDX ENTERPRISE SERVICE CONFIGURATION ######################
# The Open edX Enterprise service is currently hosted via the LMS container/process.
# However, for all intents and purposes this service is treated as a standalone IDA.
# These configuration settings are specific to the Enterprise service and you should
# not find references to them within the edx-platform project.

# Publicly-accessible enrollment URL, for use on the client side.
ENTERPRISE_PUBLIC_ENROLLMENT_API_URL = config(
    "ENTERPRISE_PUBLIC_ENROLLMENT_API_URL",
    default=(LMS_ROOT_URL or "") + LMS_ENROLLMENT_API_PATH,
)

# Enrollment URL used on the server-side.
ENTERPRISE_ENROLLMENT_API_URL = config(
    "ENTERPRISE_ENROLLMENT_API_URL",
    default=(LMS_INTERNAL_ROOT_URL or "") + LMS_ENROLLMENT_API_PATH,
)

# Enterprise logo image size limit in KB's
ENTERPRISE_CUSTOMER_LOGO_IMAGE_SIZE = config(
    "ENTERPRISE_CUSTOMER_LOGO_IMAGE_SIZE",
    default=ENTERPRISE_CUSTOMER_LOGO_IMAGE_SIZE,
    formatter=int,
)

# Course enrollment modes to be hidden in the Enterprise enrollment page
# if the "Hide audit track" flag is enabled for an EnterpriseCustomer
ENTERPRISE_COURSE_ENROLLMENT_AUDIT_MODES = config(
    "ENTERPRISE_COURSE_ENROLLMENT_AUDIT_MODES",
    default=ENTERPRISE_COURSE_ENROLLMENT_AUDIT_MODES,
    formatter=json.loads,
)

# A support URL used on Enterprise landing pages for when a warning
# message goes off.
ENTERPRISE_SUPPORT_URL = config(
    "ENTERPRISE_SUPPORT_URL", default=ENTERPRISE_SUPPORT_URL
)

# A shared secret to be used for encrypting passwords passed from the enterprise api
# to the enteprise reporting script.
ENTERPRISE_REPORTING_SECRET = config(
    "ENTERPRISE_REPORTING_SECRET", default=ENTERPRISE_REPORTING_SECRET
)

############## ENTERPRISE SERVICE API CLIENT CONFIGURATION ######################
# The LMS communicates with the Enterprise service via the EdxRestApiClient class
# The below environmental settings are utilized by the LMS when interacting with
# the service, and override the default parameters which are defined in common.py

DEFAULT_ENTERPRISE_API_URL = None
if LMS_INTERNAL_ROOT_URL is not None:
    DEFAULT_ENTERPRISE_API_URL = LMS_INTERNAL_ROOT_URL + "/enterprise/api/v1/"
ENTERPRISE_API_URL = config("ENTERPRISE_API_URL", default=DEFAULT_ENTERPRISE_API_URL)

DEFAULT_ENTERPRISE_CONSENT_API_URL = None
if LMS_INTERNAL_ROOT_URL is not None:
    DEFAULT_ENTERPRISE_CONSENT_API_URL = LMS_INTERNAL_ROOT_URL + "/consent/api/v1/"
ENTERPRISE_CONSENT_API_URL = config(
    "ENTERPRISE_CONSENT_API_URL", default=DEFAULT_ENTERPRISE_CONSENT_API_URL
)

ENTERPRISE_SERVICE_WORKER_USERNAME = config(
    "ENTERPRISE_SERVICE_WORKER_USERNAME", default=ENTERPRISE_SERVICE_WORKER_USERNAME
)
ENTERPRISE_API_CACHE_TIMEOUT = config(
    "ENTERPRISE_API_CACHE_TIMEOUT", default=ENTERPRISE_API_CACHE_TIMEOUT, formatter=int
)

############## ENTERPRISE SERVICE LMS CONFIGURATION ##################################
# The LMS has some features embedded that are related to the Enterprise service, but
# which are not provided by the Enterprise service. These settings override the
# base values for the parameters as defined in common.py

ENTERPRISE_PLATFORM_WELCOME_TEMPLATE = config(
    "ENTERPRISE_PLATFORM_WELCOME_TEMPLATE", default=ENTERPRISE_PLATFORM_WELCOME_TEMPLATE
)
ENTERPRISE_SPECIFIC_BRANDED_WELCOME_TEMPLATE = config(
    "ENTERPRISE_SPECIFIC_BRANDED_WELCOME_TEMPLATE",
    default=ENTERPRISE_SPECIFIC_BRANDED_WELCOME_TEMPLATE,
)
ENTERPRISE_TAGLINE = config("ENTERPRISE_TAGLINE", default=ENTERPRISE_TAGLINE)
ENTERPRISE_EXCLUDED_REGISTRATION_FIELDS = set(
    config(
        "ENTERPRISE_EXCLUDED_REGISTRATION_FIELDS",
        default=ENTERPRISE_EXCLUDED_REGISTRATION_FIELDS,
        formatter=json.loads,
    )
)
BASE_COOKIE_DOMAIN = config("BASE_COOKIE_DOMAIN", default=BASE_COOKIE_DOMAIN)

############## CATALOG/DISCOVERY SERVICE API CLIENT CONFIGURATION ######################
# The LMS communicates with the Catalog service via the EdxRestApiClient class
# The below environmental settings are utilized by the LMS when interacting with
# the service, and override the default parameters which are defined in common.py

COURSES_API_CACHE_TIMEOUT = config(
    "COURSES_API_CACHE_TIMEOUT", default=COURSES_API_CACHE_TIMEOUT, formatter=int
)

# Add an ICP license for serving content in China if your organization is registered to do so
ICP_LICENSE = config("ICP_LICENSE", default=None, formatter=bool)

############## Settings for CourseGraph ############################
COURSEGRAPH_JOB_QUEUE = config("COURSEGRAPH_JOB_QUEUE", default=LOW_PRIORITY_QUEUE)

########################## Parental controls config  #######################

# The age at which a learner no longer requires parental consent, or None
# if parental consent is never required.
PARENTAL_CONSENT_AGE_LIMIT = config(
    "PARENTAL_CONSENT_AGE_LIMIT", default=PARENTAL_CONSENT_AGE_LIMIT, formatter=int
)

# Do NOT calculate this dynamically at startup with git because it's *slow*.
EDX_PLATFORM_REVISION = config("EDX_PLATFORM_REVISION", default=EDX_PLATFORM_REVISION)

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
# The time a block needs to be viewed to be considered complete, in milliseconds.
COMPLETION_BY_VIEWING_DELAY_MS = config(
    "COMPLETION_BY_VIEWING_DELAY_MS",
    default=COMPLETION_BY_VIEWING_DELAY_MS,
    formatter=int,
)

############### Settings for django-fernet-fields ##################
FERNET_KEYS = config("FERNET_KEYS", default=FERNET_KEYS, formatter=json.loads)

################# Settings for the maintenance banner #################
MAINTENANCE_BANNER_TEXT = config("MAINTENANCE_BANNER_TEXT", default=None)

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

############################### Plugin Settings ###############################

from openedx.core.djangoapps.plugins import (
    plugin_settings,
    constants as plugin_constants,
)

plugin_settings.add_plugins(
    __name__, plugin_constants.ProjectType.LMS, plugin_constants.SettingsType.AWS
)

########################## Derive Any Derived Settings  #######################

derive_settings(__name__)
