"""
This is the default template for our main set of servers. This does NOT
cover the content machines, which use content.py

Common traits:
* Use memcached, and cache-backed sessions
* Use a MySQL 5.1 database
"""

# We intentionally define lots of variables that aren't used, and
# want to import all variables from base settings files
# pylint: disable=wildcard-import, unused-wildcard-import

# Pylint gets confused by path.py instances, which report themselves as class
# objects. As a result, pylint applies the wrong regex in validating names,
# and throws spurious errors. Therefore, we disable invalid-name checking.
# pylint: disable=invalid-name

import datetime
import dateutil
import json
import os
import platform

from openedx.core.lib.logsettings import get_logger_config
from path import Path as path
from xmodule.modulestore.modulestore_settings import (
    convert_module_store_setting_if_needed,
    update_module_store_settings,
)

from ..common import *
from .utils import Configuration


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


################################ ALWAYS THE SAME ##############################

RELEASE = config("RELEASE", default=None)
DEBUG = False
DEFAULT_TEMPLATE_ENGINE["OPTIONS"]["debug"] = False

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

MEDIA_ROOT = path("/edx/var/edxapp/media/")
MEDIA_URL = "/media/"

LOG_DIR = config("LOG_DIR", default=path("/edx/var/logs/edx"), formatter=path)
DATA_DIR = config("DATA_DIR", default=path("/edx/app/edxapp/data"), formatter=path)

# DEFAULT_COURSE_ABOUT_IMAGE_URL specifies the default image to show for courses that don't provide one
DEFAULT_COURSE_ABOUT_IMAGE_URL = config(
    "DEFAULT_COURSE_ABOUT_IMAGE_URL", default=DEFAULT_COURSE_ABOUT_IMAGE_URL
)


PLATFORM_NAME = config("PLATFORM_NAME", default=PLATFORM_NAME)
# For displaying on the receipt. At Stanford PLATFORM_NAME != MERCHANT_NAME, but PLATFORM_NAME is a fine default
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
EMAIL_PORT = config("EMAIL_PORT", default=25)  # django default is 25
EMAIL_USE_TLS = config("EMAIL_USE_TLS", default=False)  # django default is False
SITE_NAME = config("SITE_NAME", default=None)
HTTPS = config("HTTPS", default=HTTPS)

SESSION_ENGINE = config(
    "SESSION_ENGINE", default="django.contrib.sessions.backends.cache"
)
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
BULK_EMAIL_ROUTING_KEY_SMALL_JOBS = LOW_PRIORITY_QUEUE

# Theme overrides
THEME_NAME = config("THEME_NAME", default=None)
COMPREHENSIVE_THEME_DIR = path(
    config("COMPREHENSIVE_THEME_DIR", default=COMPREHENSIVE_THEME_DIR)
)

# Marketing link overrides
MKTG_URL_LINK_MAP = config("MKTG_URL_LINK_MAP", default={}, formatter=json.loads)

SUPPORT_SITE_LINK = config("SUPPORT_SITE_LINK", default=SUPPORT_SITE_LINK)

# Mobile store URL overrides
MOBILE_STORE_URLS = config("MOBILE_STORE_URLS", default=MOBILE_STORE_URLS)

# Timezone overrides
TIME_ZONE = config("TIME_ZONE", default=TIME_ZONE)

# Translation overrides
LANGUAGES = config("LANGUAGES", default=LANGUAGES, formatter=json.loads)
LANGUAGE_DICT = dict(LANGUAGES)
LANGUAGE_CODE = config("LANGUAGE_CODE", default=LANGUAGE_CODE)
USE_I18N = config("USE_I18N", default=USE_I18N)

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
SUBDOMAIN_BRANDING = config("SUBDOMAIN_BRANDING", default={}, formatter=json.loads)
VIRTUAL_UNIVERSITIES = config("VIRTUAL_UNIVERSITIES", default=[])
META_UNIVERSITIES = config("META_UNIVERSITIES", default={}, formatter=json.loads)
COMMENTS_SERVICE_URL = config("COMMENTS_SERVICE_URL", default="")
COMMENTS_SERVICE_KEY = config("COMMENTS_SERVICE_KEY", default="")
CERT_NAME_SHORT = config("CERT_NAME_SHORT", default=CERT_NAME_SHORT)
CERT_NAME_LONG = config("CERT_NAME_LONG", default=CERT_NAME_LONG)
CERT_QUEUE = config("CERT_QUEUE", default="test-pull")
ZENDESK_URL = config("ZENDESK_URL", default=None)
FEEDBACK_SUBMISSION_EMAIL = config("FEEDBACK_SUBMISSION_EMAIL", default=None)
MKTG_URLS = config("MKTG_URLS", default=MKTG_URLS, formatter=json.loads)

# Badgr API
BADGR_API_TOKEN = config("BADGR_API_TOKEN", default=BADGR_API_TOKEN)
BADGR_BASE_URL = config("BADGR_BASE_URL", default=BADGR_BASE_URL)
BADGR_ISSUER_SLUG = config("BADGR_ISSUER_SLUG", default=BADGR_ISSUER_SLUG)

# git repo loading  environment
GIT_REPO_DIR = config(
    "GIT_REPO_DIR", default=path("/edx/var/edxapp/course_repos"), formatter=path
)
GIT_IMPORT_STATIC = config("GIT_IMPORT_STATIC", default=True)

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

LOCALE_PATHS = config("LOCALE_PATHS", default=LOCALE_PATHS, formatter=json.loads)

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
VIDEO_CDN_URL = config("VIDEO_CDN_URL", default={}, formatter=json.loads)

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


# Field overrides.  To use the IDDE feature, add
# 'courseware.student_field_overrides.IndividualStudentOverrideProvider'.
FIELD_OVERRIDE_PROVIDERS = tuple(
    config("FIELD_OVERRIDE_PROVIDERS", default=[], formatter=json.loads)
)

############################## SECURE AUTH ITEMS ###############
# Secret things: passwords, access keys, etc.

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

############### Module Store Items ##########
HOSTNAME_MODULESTORE_DEFAULT_MAPPINGS = config(
    "HOSTNAME_MODULESTORE_DEFAULT_MAPPINGS", default={}, formatter=json.loads
)

# PREVIEW DOMAIN must be present in HOSTNAME_MODULESTORE_DEFAULT_MAPPINGS for the preview to show draft changes
if "PREVIEW_LMS_BASE" in FEATURES and FEATURES["PREVIEW_LMS_BASE"] != "":
    PREVIEW_DOMAIN = FEATURES["PREVIEW_LMS_BASE"].split(":")[0]
    # update dictionary with preview domain regex
    HOSTNAME_MODULESTORE_DEFAULT_MAPPINGS.update({PREVIEW_DOMAIN: "draft-preferred"})

############### Mixed Related(Secure/Not-Secure) Items ##########
LMS_SEGMENT_KEY = config("LMS_SEGMENT_KEY", default=None)

CC_PROCESSOR_NAME = config("CC_PROCESSOR_NAME", default=CC_PROCESSOR_NAME)
CC_PROCESSOR = config("CC_PROCESSOR", default=CC_PROCESSOR)

SECRET_KEY = config("SECRET_KEY", default="ThisisAnExampleKeyForDevPurposeOnly")

# Authentication backends
# - behind a proxy, use: "lms.envs.fun.backends.ProxyRateLimitModelBackend"
# - for LTI provider, add: "lti_provider.users.LtiBackend"
# - for CAS, add: "django_cas.backends.CASBackend"
AUTHENTICATION_BACKENDS = config(
    "AUTHENTICATION_BACKENDS", default=AUTHENTICATION_BACKENDS
)

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

# Enable automatic transaction management on all databases
# https://docs.djangoproject.com/en/1.8/topics/db/transactions/#tying-transactions-to-http-requests
# This needs to be true for all databases
for database_name in DATABASES:
    DATABASES[database_name]["ATOMIC_REQUESTS"] = True

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

EMAIL_HOST_USER = config("EMAIL_HOST_USER", default="")  # django default is ''
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD", default="")  # django default is ''

# Datadog for events!
DATADOG = config("DATADOG", default={}, formatter=json.loads)

# TODO: deprecated (compatibility with previous settings)
DATADOG_API = config("DATADOG_API", default=None)

# Analytics dashboard server
ANALYTICS_SERVER_URL = config("ANALYTICS_SERVER_URL", default=None)
ANALYTICS_API_KEY = config("ANALYTICS_API_KEY", default="")

# Analytics data source
ANALYTICS_DATA_URL = config("ANALYTICS_DATA_URL", default=ANALYTICS_DATA_URL)
ANALYTICS_DATA_TOKEN = config("ANALYTICS_DATA_TOKEN", default=ANALYTICS_DATA_TOKEN)

# Analytics Dashboard
ANALYTICS_DASHBOARD_URL = config(
    "ANALYTICS_DASHBOARD_URL", default=ANALYTICS_DASHBOARD_URL
)
ANALYTICS_DASHBOARD_NAME = config(
    "ANALYTICS_DASHBOARD_NAME", default=PLATFORM_NAME + " Insights"
)

# Mailchimp New User List
MAILCHIMP_NEW_USER_LIST_ID = config("MAILCHIMP_NEW_USER_LIST_ID", default=None)

# Zendesk
ZENDESK_USER = config("ZENDESK_USER", default=None)
ZENDESK_API_KEY = config("ZENDESK_API_KEY", default=None)

# API Key for inbound requests from Notifier service
EDX_API_KEY = config("EDX_API_KEY", default=None)

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

# Student identity verification settings
VERIFY_STUDENT = config("VERIFY_STUDENT", default=VERIFY_STUDENT, formatter=json.loads)

# Grades download
GRADES_DOWNLOAD_ROUTING_KEY = config(
    "GRADES_DOWNLOAD_ROUTING_KEY", default=HIGH_MEM_QUEUE
)

GRADES_DOWNLOAD = config(
    "GRADES_DOWNLOAD", default=GRADES_DOWNLOAD, formatter=json.loads
)

GRADES_DOWNLOAD = config("GRADES_DOWNLOAD", default=GRADES_DOWNLOAD)

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

MICROSITE_CONFIGURATION = config(
    "MICROSITE_CONFIGURATION", default={}, formatter=json.loads
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

##### LMS DEADLINE DISPLAY TIME_ZONE #######
TIME_ZONE_DISPLAYED_FOR_DEADLINES = config(
    "TIME_ZONE_DISPLAYED_FOR_DEADLINES", default=TIME_ZONE_DISPLAYED_FOR_DEADLINES
)

##### X-Frame-Options response header settings #####
X_FRAME_OPTIONS = config("X_FRAME_OPTIONS", default=X_FRAME_OPTIONS)

##### Third-party auth options ################################################
if FEATURES.get("ENABLE_THIRD_PARTY_AUTH"):
    # The reduced session expiry time during the third party login pipeline. (Value in seconds)
    SOCIAL_AUTH_PIPELINE_TIMEOUT = config("SOCIAL_AUTH_PIPELINE_TIMEOUT", default=600)

    # The SAML private/public key values do not need the delimiter lines (such as
    # "-----BEGIN PRIVATE KEY-----", default="-----END PRIVATE KEY-----" etc.) but they may be included
    # if you want (though it's easier to format the key values as JSON without the delimiters).
    SOCIAL_AUTH_SAML_SP_PRIVATE_KEY = config(
        "SOCIAL_AUTH_SAML_SP_PRIVATE_KEY", default=""
    )
    SOCIAL_AUTH_SAML_SP_PUBLIC_CERT = config(
        "SOCIAL_AUTH_SAML_SP_PUBLIC_CERT", default=""
    )
    SOCIAL_AUTH_OAUTH_SECRETS = config(
        "SOCIAL_AUTH_OAUTH_SECRETS", default={}, formatter=json.loads
    )
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
    OAUTH_OIDC_ISSUER = config("OAUTH_OIDC_ISSUER", default=None)
    OAUTH_ENFORCE_SECURE = config("OAUTH_ENFORCE_SECURE", default=True, formatter=bool)
    OAUTH_ENFORCE_CLIENT_SECURE = config(
        "OAUTH_ENFORCE_CLIENT_SECURE", default=True, formatter=bool
    )

##### ADVANCED_SECURITY_CONFIG #####
ADVANCED_SECURITY_CONFIG = config(
    "ADVANCED_SECURITY_CONFIG", default={}, formatter=json.loads
)

##### GOOGLE ANALYTICS IDS #####
GOOGLE_ANALYTICS_ACCOUNT = config("GOOGLE_ANALYTICS_ACCOUNT", default=None)
GOOGLE_ANALYTICS_LINKEDIN = config("GOOGLE_ANALYTICS_LINKEDIN", default=None)

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
FACEBOOK_APP_SECRET = config("FACEBOOK_APP_SECRET", default=None)
FACEBOOK_APP_ID = config("FACEBOOK_APP_ID", default=None)

XBLOCK_SETTINGS = config("XBLOCK_SETTINGS", default={}, formatter=json.loads)
XBLOCK_SETTINGS.setdefault("VideoDescriptor", {})["licensing_enabled"] = FEATURES.get(
    "LICENSING", False
)
XBLOCK_SETTINGS.setdefault("VideoModule", {})["YOUTUBE_API_KEY"] = config(
    "YOUTUBE_API_KEY", default=YOUTUBE_API_KEY
)

##### CDN EXPERIMENT/MONITORING FLAGS #####
CDN_VIDEO_URLS = config("CDN_VIDEO_URLS", default=CDN_VIDEO_URLS)
ONLOAD_BEACON_SAMPLE_RATE = config(
    "ONLOAD_BEACON_SAMPLE_RATE", default=ONLOAD_BEACON_SAMPLE_RATE
)

##### ECOMMERCE API CONFIGURATION SETTINGS #####
ECOMMERCE_PUBLIC_URL_ROOT = config(
    "ECOMMERCE_PUBLIC_URL_ROOT", default=ECOMMERCE_PUBLIC_URL_ROOT
)
ECOMMERCE_API_URL = config("ECOMMERCE_API_URL", default=ECOMMERCE_API_URL)
ECOMMERCE_API_TIMEOUT = config(
    "ECOMMERCE_API_TIMEOUT", default=ECOMMERCE_API_TIMEOUT, formatter=int
)

ECOMMERCE_SERVICE_WORKER_USERNAME = config(
    "ECOMMERCE_SERVICE_WORKER_USERNAME", default=ECOMMERCE_SERVICE_WORKER_USERNAME
)
ECOMMERCE_API_TIMEOUT = config("ECOMMERCE_API_TIMEOUT", default=ECOMMERCE_API_TIMEOUT)

##### Custom Courses for EdX #####
if FEATURES.get("CUSTOM_COURSES_EDX"):
    INSTALLED_APPS += ("lms.djangoapps.ccx",)
    FIELD_OVERRIDE_PROVIDERS += (
        "lms.djangoapps.ccx.overrides.CustomCoursesForEdxOverrideProvider",
    )
CCX_MAX_STUDENTS_ALLOWED = config(
    "CCX_MAX_STUDENTS_ALLOWED", default=CCX_MAX_STUDENTS_ALLOWED
)

##### Individual Due Date Extensions #####
if FEATURES.get("INDIVIDUAL_DUE_DATES"):
    FIELD_OVERRIDE_PROVIDERS += (
        "courseware.student_field_overrides.IndividualStudentOverrideProvider",
    )

##### Self-Paced Course Due Dates #####
FIELD_OVERRIDE_PROVIDERS += (
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

# EdxNotes config

EDXNOTES_PUBLIC_API = config("EDXNOTES_PUBLIC_API", default=EDXNOTES_PUBLIC_API)
EDXNOTES_INTERNAL_API = config("EDXNOTES_INTERNAL_API", default=EDXNOTES_INTERNAL_API)

##### Credit Provider Integration #####

CREDIT_PROVIDER_SECRET_KEYS = config(
    "CREDIT_PROVIDER_SECRET_KEYS", default={}, formatter=json.loads
)

##################### LTI Provider #####################
if FEATURES.get("ENABLE_LTI_PROVIDER"):
    INSTALLED_APPS += ("lti_provider",)

LTI_USER_EMAIL_DOMAIN = config("LTI_USER_EMAIL_DOMAIN", default="lti.example.com")

# For more info on this, see the notes in common.py
LTI_AGGREGATE_SCORE_PASSBACK_DELAY = config(
    "LTI_AGGREGATE_SCORE_PASSBACK_DELAY", default=LTI_AGGREGATE_SCORE_PASSBACK_DELAY
)

##################### Credit Provider help link ####################
CREDIT_HELP_LINK_URL = config("CREDIT_HELP_LINK_URL", default=CREDIT_HELP_LINK_URL)

#### JWT configuration ####
JWT_ISSUER = config("JWT_ISSUER", default=JWT_ISSUER)
JWT_EXPIRATION = config("JWT_EXPIRATION", default=JWT_EXPIRATION)

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

# Cutoff date for granting audit certificates
if config("AUDIT_CERT_CUTOFF_DATE", default=None):
    AUDIT_CERT_CUTOFF_DATE = dateutil.parser.parse(
        config("AUDIT_CERT_CUTOFF_DATE", default=AUDIT_CERT_CUTOFF_DATE)
    )
