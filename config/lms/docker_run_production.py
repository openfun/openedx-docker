# -*- coding: utf-8 -*-

"""
This is the settings to run Open edX with Docker the FUN way.
"""

import datetime
import dateutil
import json
import os
import platform
import warnings

from path import Path as path
from xmodule.modulestore.modulestore_settings import convert_module_store_setting_if_needed

from ..common import *
from .utils import Configuration


# Load custom configuration parameters from yaml files
config = Configuration(os.path.dirname(__file__))

################################ ALWAYS THE SAME ##############################

DEBUG = False
DEFAULT_TEMPLATE_ENGINE['OPTIONS']['debug'] = False

SESSION_ENGINE = config('SESSION_ENGINE', default='django.contrib.sessions.backends.cache')

# IMPORTANT: With this enabled, the server must always be behind a proxy that
# strips the header HTTP_X_FORWARDED_PROTO from client requests. Otherwise,
# a user can fool our server into thinking it was an https connection.
# See
# https://docs.djangoproject.com/en/dev/ref/settings/#secure-proxy-ssl-header
# for other warnings.
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

###################################### CELERY  ################################

# Don't use a connection pool, since connections are dropped by ELB.
BROKER_POOL_LIMIT = 0
BROKER_CONNECTION_TIMEOUT = 1

# For the Result Store, use the django cache named 'celery'
CELERY_RESULT_BACKEND = 'djcelery.backends.cache:CacheBackend'

# When the broker is behind an ELB, use a heartbeat to refresh the
# connection and to detect if it has been dropped.
BROKER_HEARTBEAT = 10.0
BROKER_HEARTBEAT_CHECKRATE = 2

# Each worker should only fetch one message at a time
CELERYD_PREFETCH_MULTIPLIER = 1

# Celery queues

DEFAULT_PRIORITY_QUEUE = config(
    "DEFAULT_PRIORITY_QUEUE", default="edx.lms.core.default")
HIGH_PRIORITY_QUEUE = config(
    "HIGH_PRIORITY_QUEUE", default="edx.lms.core.high")
LOW_PRIORITY_QUEUE = config(
    "LOW_PRIORITY_QUEUE", default="edx.lms.core.low")
HIGH_MEM_QUEUE = config(
    "HIGH_MEM_QUEUE", default="edx.lms.core.high_mem")

CELERY_QUEUES = config("CELERY_QUEUES", default={
    DEFAULT_PRIORITY_QUEUE: {},
    HIGH_PRIORITY_QUEUE: {},
    LOW_PRIORITY_QUEUE: {},
    HIGH_MEM_QUEUE: {},
})

CELERY_ROUTES = 'lms.celery.Router'

# Force accepted content to "json" only. If we also accept pickle-serialized
# messages, the worker will crash when it's running with a privileged user (even
# if it's not the root user but a user belonging to the root group, which is our
# case with OpenShift).
CELERY_ACCEPT_CONTENT = ['json']

# If we're a worker on the high_mem queue, set ourselves to die after processing
# one request to avoid having memory leaks take down the worker server. This env
# var is set in /etc/init/edx-workers.conf -- this should probably be replaced
# with some celery API call to see what queue we started listening to, but I
# don't know what that call is or if it's active at this point in the code.
if os.environ.get('QUEUE') == 'high_mem':
    CELERYD_MAX_TASKS_PER_CHILD = 1

CELERYBEAT_SCHEDULE = {}  # For scheduling tasks, entries can be added to this dict

########################## NON-SECURE ENV CONFIG ##############################
# Things like server locations, ports, etc.

STATIC_URL = '/static/'
STATIC_ROOT = path('/edx/app/edxapp/staticfiles')

WEBPACK_LOADER['DEFAULT']['STATS_FILE'] = STATIC_ROOT / "webpack-stats.json"

PLATFORM_NAME = config('PLATFORM_NAME', default=PLATFORM_NAME)
PLATFORM_TWITTER_ACCOUNT = config('PLATFORM_TWITTER_ACCOUNT', default=PLATFORM_TWITTER_ACCOUNT)
PLATFORM_FACEBOOK_ACCOUNT = config('PLATFORM_FACEBOOK_ACCOUNT', default=PLATFORM_FACEBOOK_ACCOUNT)
SOCIAL_SHARING_SETTINGS = config('SOCIAL_SHARING_SETTINGS', default=SOCIAL_SHARING_SETTINGS)

# Social media links for the page footer
SOCIAL_MEDIA_FOOTER_URLS = config('SOCIAL_MEDIA_FOOTER_URLS', default=SOCIAL_MEDIA_FOOTER_URLS)

CC_MERCHANT_NAME = config('CC_MERCHANT_NAME', default=PLATFORM_NAME)
EMAIL_BACKEND = config('EMAIL_BACKEND', default=EMAIL_BACKEND)
EMAIL_FILE_PATH = config('EMAIL_FILE_PATH', default=None)
EMAIL_HOST = config('EMAIL_HOST', default='localhost') # django default is localhost
EMAIL_PORT = config('EMAIL_PORT', default=25) # django default is 25
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=False) # django default is False
SITE_NAME = config('SITE_NAME', default=SITE_NAME)
HTTPS = config('HTTPS', default=HTTPS)
SESSION_COOKIE_DOMAIN = config('SESSION_COOKIE_DOMAIN', default=None)
SESSION_COOKIE_HTTPONLY = config('SESSION_COOKIE_HTTPONLY', default=True)
SESSION_COOKIE_SECURE = config('SESSION_COOKIE_SECURE', default=SESSION_COOKIE_SECURE)
SESSION_SAVE_EVERY_REQUEST = config(
    'SESSION_SAVE_EVERY_REQUEST',
    default=SESSION_SAVE_EVERY_REQUEST
)

REGISTRATION_EXTRA_FIELDS = config('REGISTRATION_EXTRA_FIELDS', default=REGISTRATION_EXTRA_FIELDS)
REGISTRATION_EXTENSION_FORM = config(
    'REGISTRATION_EXTENSION_FORM',
    default=REGISTRATION_EXTENSION_FORM
)
REGISTRATION_EMAIL_PATTERNS_ALLOWED = config('REGISTRATION_EMAIL_PATTERNS_ALLOWED', default=None)
REGISTRATION_FIELD_ORDER = config('REGISTRATION_FIELD_ORDER', default=REGISTRATION_FIELD_ORDER)

# Set the names of cookies shared with the marketing site
# These have the same cookie domain as the session, which in production
# usually includes subdomains.
EDXMKTG_LOGGED_IN_COOKIE_NAME = config(
    'EDXMKTG_LOGGED_IN_COOKIE_NAME',
    default=EDXMKTG_LOGGED_IN_COOKIE_NAME
)
EDXMKTG_USER_INFO_COOKIE_NAME = config(
    'EDXMKTG_USER_INFO_COOKIE_NAME',
    default=EDXMKTG_USER_INFO_COOKIE_NAME
)

LMS_ROOT_URL = config('LMS_ROOT_URL', default='http://localhost:8000')
LMS_INTERNAL_ROOT_URL = config('LMS_INTERNAL_ROOT_URL', default=LMS_ROOT_URL)

# Override feature by feature by whatever is being redefined in the settings.yaml file
CONFIG_FEATURES = config('FEATURES', default={})
FEATURES.update(CONFIG_FEATURES)

LMS_BASE = config('LMS_BASE', default='localhost:8072')
CMS_BASE = config('CMS_BASE', default='localhost:8082')

ALLOWED_HOSTS = [LMS_BASE.split(':')[0]]
if FEATURES.get('PREVIEW_LMS_BASE'):
    ALLOWED_HOSTS.append(FEATURES['PREVIEW_LMS_BASE'])

# allow for environments to specify what cookie name our login subsystem should use
# this is to fix a bug regarding simultaneous logins between edx.org and edge.edx.org which can
# happen with some browsers (e.g. Firefox)
if config('SESSION_COOKIE_NAME', default=None):
    # NOTE, there's a bug in Django (http://bugs.python.org/issue18012) which necessitates this
    # being a str()
    SESSION_COOKIE_NAME = str(config('SESSION_COOKIE_NAME'))

LOG_DIR = config('LOG_DIR', default='/edx/var/logs/edx')

CACHES = config('CACHES', default={
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
})

# Cache used for location mapping -- called many times with the same key/value
# in a given request.
if 'loc_cache' not in CACHES:
    CACHES['loc_cache'] = {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'edx_location_mem_cache',
    }

# Email overrides
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default=DEFAULT_FROM_EMAIL)
DEFAULT_FEEDBACK_EMAIL = config('DEFAULT_FEEDBACK_EMAIL', default=DEFAULT_FEEDBACK_EMAIL)
ADMINS = config('ADMINS', default=ADMINS)
SERVER_EMAIL = config('SERVER_EMAIL', default=SERVER_EMAIL)
TECH_SUPPORT_EMAIL = config('TECH_SUPPORT_EMAIL', default=TECH_SUPPORT_EMAIL)
CONTACT_EMAIL = config('CONTACT_EMAIL', default=CONTACT_EMAIL)
BUGS_EMAIL = config('BUGS_EMAIL', default=BUGS_EMAIL)
PAYMENT_SUPPORT_EMAIL = config('PAYMENT_SUPPORT_EMAIL', default=PAYMENT_SUPPORT_EMAIL)
FINANCE_EMAIL = config('FINANCE_EMAIL', default=FINANCE_EMAIL)
UNIVERSITY_EMAIL = config('UNIVERSITY_EMAIL', default=UNIVERSITY_EMAIL)
PRESS_EMAIL = config('PRESS_EMAIL', default=PRESS_EMAIL)

CONTACT_MAILING_ADDRESS = config('CONTACT_MAILING_ADDRESS', default=CONTACT_MAILING_ADDRESS)

# Account activation email sender address
ACTIVATION_EMAIL_FROM_ADDRESS = config(
    'ACTIVATION_EMAIL_FROM_ADDRESS',
    default=DEFAULT_FROM_EMAIL)

# Currency
PAID_COURSE_REGISTRATION_CURRENCY = config(
    'PAID_COURSE_REGISTRATION_CURRENCY',
    default=PAID_COURSE_REGISTRATION_CURRENCY
)

# Payment Report Settings
PAYMENT_REPORT_GENERATOR_GROUP = config(
    'PAYMENT_REPORT_GENERATOR_GROUP',
    default=PAYMENT_REPORT_GENERATOR_GROUP
)

# Bulk Email overrides
BULK_EMAIL_DEFAULT_FROM_EMAIL = config(
    'BULK_EMAIL_DEFAULT_FROM_EMAIL',
    default=BULK_EMAIL_DEFAULT_FROM_EMAIL
)
BULK_EMAIL_EMAILS_PER_TASK = config(
    'BULK_EMAIL_EMAILS_PER_TASK',
    default=BULK_EMAIL_EMAILS_PER_TASK
)
BULK_EMAIL_DEFAULT_RETRY_DELAY = config(
    'BULK_EMAIL_DEFAULT_RETRY_DELAY',
    default=BULK_EMAIL_DEFAULT_RETRY_DELAY
)
BULK_EMAIL_MAX_RETRIES = config(
    'BULK_EMAIL_MAX_RETRIES',
    default=BULK_EMAIL_MAX_RETRIES
)
BULK_EMAIL_INFINITE_RETRY_CAP = config(
    'BULK_EMAIL_INFINITE_RETRY_CAP',
    default=BULK_EMAIL_INFINITE_RETRY_CAP
)
BULK_EMAIL_LOG_SENT_EMAILS = config(
    'BULK_EMAIL_LOG_SENT_EMAILS',
    default=BULK_EMAIL_LOG_SENT_EMAILS
)
BULK_EMAIL_RETRY_DELAY_BETWEEN_SENDS = config(
    'BULK_EMAIL_RETRY_DELAY_BETWEEN_SENDS',
    default=BULK_EMAIL_RETRY_DELAY_BETWEEN_SENDS
)
# We want Bulk Email running on the high-priority queue, so we define the
# routing key that points to it. At the moment, the name is the same.
# We have to reset the value here, since we have changed the value of the queue name.
BULK_EMAIL_ROUTING_KEY = config(
    'BULK_EMAIL_ROUTING_KEY',
    default=HIGH_PRIORITY_QUEUE
)

# We can run smaller jobs on the low priority queue. See note above for why
# we have to reset the value here.
BULK_EMAIL_ROUTING_KEY_SMALL_JOBS = config(
    'BULK_EMAIL_ROUTING_KEY_SMALL_JOBS',
    default=LOW_PRIORITY_QUEUE
)

# Queue to use for updating persistent grades
RECALCULATE_GRADES_ROUTING_KEY = config(
    'RECALCULATE_GRADES_ROUTING_KEY',
    default=LOW_PRIORITY_QUEUE
)

# Message expiry time in seconds
CELERY_EVENT_QUEUE_TTL = config('CELERY_EVENT_QUEUE_TTL', default=None)

# following setting is for backward compatibility
if config('COMPREHENSIVE_THEME_DIR', default=None):
    COMPREHENSIVE_THEME_DIR = config('COMPREHENSIVE_THEME_DIR')

COMPREHENSIVE_THEME_DIRS = config(
    'COMPREHENSIVE_THEME_DIRS',
    default=COMPREHENSIVE_THEME_DIRS
) or []

# COMPREHENSIVE_THEME_LOCALE_PATHS contain the paths to themes locale directories e.g.
# "COMPREHENSIVE_THEME_LOCALE_PATHS" : [
#        "/edx/src/edx-themes/conf/locale"
#    ],
COMPREHENSIVE_THEME_LOCALE_PATHS = config(
    'COMPREHENSIVE_THEME_LOCALE_PATHS',
    default=[]
)

DEFAULT_SITE_THEME = config(
    'DEFAULT_SITE_THEME',
    default=DEFAULT_SITE_THEME
)
ENABLE_COMPREHENSIVE_THEMING = config(
    'ENABLE_COMPREHENSIVE_THEMING',
    default=ENABLE_COMPREHENSIVE_THEMING
)

# Marketing link overrides
MKTG_URL_LINK_MAP.update(config('MKTG_URL_LINK_MAP', default={}))

# Intentional defaults.
SUPPORT_SITE_LINK = config('SUPPORT_SITE_LINK', default=SUPPORT_SITE_LINK)
PASSWORD_RESET_SUPPORT_LINK = config('PASSWORD_RESET_SUPPORT_LINK', default=SUPPORT_SITE_LINK)
ACTIVATION_EMAIL_SUPPORT_LINK = config(
    'ACTIVATION_EMAIL_SUPPORT_LINK',
    default=SUPPORT_SITE_LINK
)

# Mobile store URL overrides
MOBILE_STORE_URLS = config('MOBILE_STORE_URLS', default=MOBILE_STORE_URLS)

# Timezone overrides
TIME_ZONE = config('TIME_ZONE', default=TIME_ZONE)

# Translation overrides
LANGUAGES = config('LANGUAGES', default=LANGUAGES)
LANGUAGE_DICT = dict(LANGUAGES)
LANGUAGE_CODE = config('LANGUAGE_CODE', default=LANGUAGE_CODE)
LANGUAGE_COOKIE = config('LANGUAGE_COOKIE', default=LANGUAGE_COOKIE)

USE_I18N = config('USE_I18N', default=USE_I18N)

# Additional installed apps
for app in config('ADDL_INSTALLED_APPS', default=[]):
    INSTALLED_APPS += (app,)

WIKI_ENABLED = config('WIKI_ENABLED', default=WIKI_ENABLED)
local_loglevel = config('LOCAL_LOGLEVEL', default='INFO')

# Configure Logging

# Default format for syslog logging
standard_format = (
     '%(asctime)s %(levelname)s %(process)d [%(name)s] %(filename)s:%(lineno)d - %(message)s'
)
syslog_format = (
    '[variant:lms][%(name)s][env:sandbox] %(levelname)s '
    '[{hostname}  %(process)d] [%(filename)s:%(lineno)d] - %(message)s'
).format(hostname=platform.node().split(".")[0])

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'local': {
            'formatter': 'syslog_format',
            'class': 'logging.StreamHandler',
            'level': 'INFO'
        },
        'tracking': {
            'formatter': 'raw',
            'class': 'logging.StreamHandler',
            'level': 'DEBUG'
        },
        'console': {
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
            'level': 'INFO'
        },
    },
    'formatters': {
        'raw': {'format': '%(message)s'},
        'syslog_format': {'format': syslog_format},
        'standard': {'format': standard_format}
    },
    'filters': {'require_debug_false': {'()': 'django.utils.log.RequireDebugFalse'}},
    'loggers': {
        '': {
            'level': 'INFO',
            'propagate': False,
            'handlers': ['console', 'local']
        },
        'tracking': {
            'level': 'DEBUG',
            'propagate': False,
            'handlers': ['tracking']
        }
    }
}

SENTRY_DSN = config('SENTRY_DSN', default=None)
if SENTRY_DSN:
    LOGGING['loggers']['']['handlers'].append('sentry')
    LOGGING['handlers']['sentry'] = {
        'class': 'raven.handlers.logging.SentryHandler',
        'dsn': SENTRY_DSN,
        'level': 'ERROR'
    }


COURSE_LISTINGS = config('COURSE_LISTINGS', default={})
VIRTUAL_UNIVERSITIES = config('VIRTUAL_UNIVERSITIES', default=[])
META_UNIVERSITIES = config('META_UNIVERSITIES', default={})
COMMENTS_SERVICE_URL = config("COMMENTS_SERVICE_URL", default='')
COMMENTS_SERVICE_KEY = config("COMMENTS_SERVICE_KEY", default='')
CERT_QUEUE = config('CERT_QUEUE', default='test-pull')

FEEDBACK_SUBMISSION_EMAIL = config('FEEDBACK_SUBMISSION_EMAIL', default=None)
MKTG_URLS = config('MKTG_URLS', default=MKTG_URLS)

# Badgr API
BADGR_API_TOKEN = config('BADGR_API_TOKEN', default=BADGR_API_TOKEN)
BADGR_BASE_URL = config('BADGR_BASE_URL', default=BADGR_BASE_URL)
BADGR_ISSUER_SLUG = config('BADGR_ISSUER_SLUG', default=BADGR_ISSUER_SLUG)
BADGR_TIMEOUT = config('BADGR_TIMEOUT', default=BADGR_TIMEOUT)

# git repo loading  environment
GIT_REPO_DIR = config('GIT_REPO_DIR', default='/edx/var/edxapp/course_repos')
GIT_IMPORT_STATIC = config('GIT_IMPORT_STATIC', default=True)

for name, value in config("CODE_JAIL", default={}).items():
    oldvalue = CODE_JAIL.get(name)
    if isinstance(oldvalue, dict):
        for subname, subvalue in value.items():
            oldvalue[subname] = subvalue
    else:
        CODE_JAIL[name] = value

COURSES_WITH_UNSAFE_CODE = config("COURSES_WITH_UNSAFE_CODE", default=[])

ASSET_IGNORE_REGEX = config('ASSET_IGNORE_REGEX', default=ASSET_IGNORE_REGEX)

# Event Tracking
TRACKING_IGNORE_URL_PATTERNS = config(
    'TRACKING_IGNORE_URL_PATTERNS',
    default=None
)

# SSL external authentication settings
SSL_AUTH_EMAIL_DOMAIN = config(
    'SSL_AUTH_EMAIL_DOMAIN',
    default='MIT.EDU'
)
SSL_AUTH_DN_FORMAT_STRING = config(
    'SSL_AUTH_DN_FORMAT_STRING',
    default=None
)

# Django CAS external authentication settings
CAS_EXTRA_LOGIN_PARAMS = config("CAS_EXTRA_LOGIN_PARAMS", default=None)
if FEATURES.get('AUTH_USE_CAS'):
    CAS_SERVER_URL = config("CAS_SERVER_URL", default=None)
    AUTHENTICATION_BACKENDS = (
        'django.contrib.auth.backends.ModelBackend',
        'django_cas.backends.CASBackend',
    )
    INSTALLED_APPS += ('django_cas',)
    MIDDLEWARE_CLASSES += ('django_cas.middleware.CASMiddleware',)
    CAS_ATTRIBUTE_CALLBACK = config('CAS_ATTRIBUTE_CALLBACK', default=None)
    if CAS_ATTRIBUTE_CALLBACK:
        import importlib
        CAS_USER_DETAILS_RESOLVER = getattr(
            importlib.import_module(CAS_ATTRIBUTE_CALLBACK['module']),
            CAS_ATTRIBUTE_CALLBACK['function']
        )

# Video Caching. Pairing country codes with CDN URLs.
# Example: {'CN': 'http://api.xuetangx.com/edx/video?s3_url='}
VIDEO_CDN_URL = config('VIDEO_CDN_URL', default={})

# Branded footer
FOOTER_OPENEDX_URL = config('FOOTER_OPENEDX_URL', default=FOOTER_OPENEDX_URL)
FOOTER_OPENEDX_LOGO_IMAGE = config('FOOTER_OPENEDX_LOGO_IMAGE', default=FOOTER_OPENEDX_LOGO_IMAGE)
FOOTER_ORGANIZATION_IMAGE = config('FOOTER_ORGANIZATION_IMAGE', default=FOOTER_ORGANIZATION_IMAGE)
FOOTER_CACHE_TIMEOUT = config('FOOTER_CACHE_TIMEOUT', default=FOOTER_CACHE_TIMEOUT)
FOOTER_BROWSER_CACHE_MAX_AGE = config(
    'FOOTER_BROWSER_CACHE_MAX_AGE',
    default=FOOTER_BROWSER_CACHE_MAX_AGE
)

# Credit notifications settings
NOTIFICATION_EMAIL_CSS = config('NOTIFICATION_EMAIL_CSS', default=NOTIFICATION_EMAIL_CSS)
NOTIFICATION_EMAIL_EDX_LOGO = config(
    'NOTIFICATION_EMAIL_EDX_LOGO',
    default=NOTIFICATION_EMAIL_EDX_LOGO
)

# Determines whether the CSRF token can be transported on
# unencrypted channels. It is set to False here for backward compatibility,
# but it is highly recommended that this is True for enviroments accessed
# by end users.
CSRF_COOKIE_SECURE = config('CSRF_COOKIE_SECURE', default=False)

############# CORS headers for cross-domain requests #################

if FEATURES.get('ENABLE_CORS_HEADERS') or FEATURES.get('ENABLE_CROSS_DOMAIN_CSRF_COOKIE'):
    CORS_ALLOW_CREDENTIALS = True
    CORS_ORIGIN_WHITELIST = config('CORS_ORIGIN_WHITELIST', default=())
    CORS_ORIGIN_ALLOW_ALL = config('CORS_ORIGIN_ALLOW_ALL', default=False)
    CORS_ALLOW_INSECURE = config('CORS_ALLOW_INSECURE', default=False)

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
    CROSS_DOMAIN_CSRF_COOKIE_NAME = str(config('CROSS_DOMAIN_CSRF_COOKIE_NAME'))

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
    CROSS_DOMAIN_CSRF_COOKIE_DOMAIN = config('CROSS_DOMAIN_CSRF_COOKIE_DOMAIN')


# Field overrides. To use the IDDE feature, add
# 'courseware.student_field_overrides.IndividualStudentOverrideProvider'.
FIELD_OVERRIDE_PROVIDERS = tuple(config('FIELD_OVERRIDE_PROVIDERS', default=[]))

############################## SECURE AUTH ITEMS ###############

############### XBlock filesystem field config ##########
DJFS = config('DJFS', default=None)

############### Module Store Items ##########
HOSTNAME_MODULESTORE_DEFAULT_MAPPINGS = config('HOSTNAME_MODULESTORE_DEFAULT_MAPPINGS', default={})
# PREVIEW DOMAIN must be present in HOSTNAME_MODULESTORE_DEFAULT_MAPPINGS for the preview to show
# draft changes
if 'PREVIEW_LMS_BASE' in FEATURES and FEATURES['PREVIEW_LMS_BASE'] != '':
    PREVIEW_DOMAIN = FEATURES['PREVIEW_LMS_BASE'].split(':')[0]
    # update dictionary with preview domain regex
    HOSTNAME_MODULESTORE_DEFAULT_MAPPINGS.update({
        PREVIEW_DOMAIN: 'draft-preferred'
    })

MODULESTORE_FIELD_OVERRIDE_PROVIDERS = config(
    'MODULESTORE_FIELD_OVERRIDE_PROVIDERS',
    default=MODULESTORE_FIELD_OVERRIDE_PROVIDERS
)

XBLOCK_FIELD_DATA_WRAPPERS = config(
    'XBLOCK_FIELD_DATA_WRAPPERS',
    default=XBLOCK_FIELD_DATA_WRAPPERS
)

############### Mixed Related(Secure/Not-Secure) Items ##########
LMS_SEGMENT_KEY = config('LMS_SEGMENT_KEY', default=None)

CC_PROCESSOR_NAME = config('CC_PROCESSOR_NAME', default=CC_PROCESSOR_NAME)
CC_PROCESSOR = config('CC_PROCESSOR', default=CC_PROCESSOR)

SECRET_KEY = config('SECRET_KEY', default='ThisIsAnExampleKeyForDevPurposeOnly')

DEFAULT_FILE_STORAGE = config(
    'DEFAULT_FILE_STORAGE',
    default='django.core.files.storage.FileSystemStorage'
)

# Specific setting for the File Upload Service to store media in a bucket.
FILE_UPLOAD_STORAGE_BUCKET_NAME = config(
    'FILE_UPLOAD_STORAGE_BUCKET_NAME',
    default=FILE_UPLOAD_STORAGE_BUCKET_NAME
)
FILE_UPLOAD_STORAGE_PREFIX = config(
    'FILE_UPLOAD_STORAGE_PREFIX',
    default=FILE_UPLOAD_STORAGE_PREFIX
)

# If there is a database called 'read_replica', you can use the use_read_replica_if_available
# function in util/query.py, which is useful for very large database reads
DATABASES = config('DATABASES', default={
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': 'mysql',
        'PORT': '3306',
        'NAME': 'edxapp',
        'USER': 'fun',
        'PASSWORD': 'password',
    }
})

XQUEUE_INTERFACE = config('XQUEUE_INTERFACE', default={
    'url': None,
    'basic_auth': None,
    'django_auth': None,
})

# Configure the MODULESTORE
MODULESTORE = convert_module_store_setting_if_needed(config('MODULESTORE', default=MODULESTORE))
DOC_STORE_CONFIG = config('DOC_STORE_CONFIG', default={
    'host': 'mongodb',
    'db': 'edxapp',
})
MONGODB_LOG = config('MONGODB_LOG', default={})
CONTENTSTORE = config('CONTENTSTORE', default={
    'DOC_STORE_CONFIG': {
        'host': ['mongodb'],
        'db': 'edxapp',
        'port': 27017
    },
    'ENGINE': 'xmodule.contentstore.mongo.MongoContentStore',
})

update_module_store_settings(MODULESTORE, doc_store_settings=DOC_STORE_CONFIG)

EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')  # django default is ''
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')  # django default is ''

# Datadog for events!
DATADOG = config('DATADOG', default={})
DATADOG.update(config('DATADOG', default={}))

# TODO: deprecated (compatibility with previous settings)
DATADOG_API = config('DATADOG_API', default=None)

# Analytics dashboard server
ANALYTICS_SERVER_URL = config('ANALYTICS_SERVER_URL', default='')
ANALYTICS_API_KEY = config('ANALYTICS_API_KEY', default='')

# Analytics data source
ANALYTICS_DATA_URL = config('ANALYTICS_DATA_URL', default=ANALYTICS_DATA_URL)
ANALYTICS_DATA_TOKEN = config('ANALYTICS_DATA_TOKEN', default=ANALYTICS_DATA_TOKEN)

# Analytics Dashboard
ANALYTICS_DASHBOARD_URL = config(
    'ANALYTICS_DASHBOARD_URL',
    default=ANALYTICS_DASHBOARD_URL
)
ANALYTICS_DASHBOARD_NAME = config(
    'ANALYTICS_DASHBOARD_NAME',
    default=PLATFORM_NAME + ' Insights'
)

# Mailchimp New User List
MAILCHIMP_NEW_USER_LIST_ID = config('MAILCHIMP_NEW_USER_LIST_ID', default=None)

# Zendesk
ZENDESK_URL = config('ZENDESK_URL', default=None)
ZENDESK_USER = config('ZENDESK_USER', default=None)
ZENDESK_API_KEY = config('ZENDESK_API_KEY', default=None)
ZENDESK_CUSTOM_FIELDS = config('ZENDESK_CUSTOM_FIELDS', default={})

# API Key for inbound requests from Notifier service
EDX_API_KEY = config('EDX_API_KEY', default='ThisIsAnExampleKeyForDevPurposeOnly')

# Celery Broker
CELERY_BROKER_TRANSPORT = config('CELERY_BROKER_TRANSPORT', default="redis")
CELERY_BROKER_USER = config('CELERY_BROKER_USER', default="")
CELERY_BROKER_PASSWORD = config('CELERY_BROKER_PASSWORD', default="")
CELERY_BROKER_HOST = config('CELERY_BROKER_HOST', default="redis")
CELERY_BROKER_PORT = config('CELERY_BROKER_PORT', default=6379)
CELERY_BROKER_VHOST = config('CELERY_BROKER_VHOST', default=0)

BROKER_URL = '{transport}://{user}:{password}@{host}:{port}/{vhost}'.format(
    transport=CELERY_BROKER_TRANSPORT,
    user=CELERY_BROKER_USER,
    password=CELERY_BROKER_PASSWORD,
    host=CELERY_BROKER_HOST,
    port=CELERY_BROKER_PORT,
    vhost=CELERY_BROKER_VHOST
)
BROKER_USE_SSL = config('CELERY_BROKER_USE_SSL', default=False)

# Block Structures
BLOCK_STRUCTURES_SETTINGS = config('BLOCK_STRUCTURES_SETTINGS', default=BLOCK_STRUCTURES_SETTINGS)

# upload limits
STUDENT_FILEUPLOAD_MAX_SIZE = config(
    'STUDENT_FILEUPLOAD_MAX_SIZE',
    default=STUDENT_FILEUPLOAD_MAX_SIZE
)

# Event tracking
TRACKING_BACKENDS.update(config('TRACKING_BACKENDS', default={}))
EVENT_TRACKING_BACKENDS['tracking_logs']['OPTIONS']['backends'].update(
    config('EVENT_TRACKING_BACKENDS', default={})
)
EVENT_TRACKING_BACKENDS['segmentio']['OPTIONS']['processors'][0]['OPTIONS']['whitelist'].extend(
    config('EVENT_TRACKING_SEGMENTIO_EMIT_WHITELIST', default=[]))
TRACKING_SEGMENTIO_WEBHOOK_SECRET = config(
    'TRACKING_SEGMENTIO_WEBHOOK_SECRET',
    default=TRACKING_SEGMENTIO_WEBHOOK_SECRET
)
TRACKING_SEGMENTIO_ALLOWED_TYPES = config(
    'TRACKING_SEGMENTIO_ALLOWED_TYPES',
    default=TRACKING_SEGMENTIO_ALLOWED_TYPES
)
TRACKING_SEGMENTIO_DISALLOWED_SUBSTRING_NAMES = config(
    'TRACKING_SEGMENTIO_DISALLOWED_SUBSTRING_NAMES',
    default=TRACKING_SEGMENTIO_DISALLOWED_SUBSTRING_NAMES
)
TRACKING_SEGMENTIO_SOURCE_MAP = config(
    'TRACKING_SEGMENTIO_SOURCE_MAP',
    default=TRACKING_SEGMENTIO_SOURCE_MAP
)

# Student identity verification settings
VERIFY_STUDENT = config('VERIFY_STUDENT', default=VERIFY_STUDENT)
DISABLE_ACCOUNT_ACTIVATION_REQUIREMENT_SWITCH = config(
    'DISABLE_ACCOUNT_ACTIVATION_REQUIREMENT_SWITCH',
    default=DISABLE_ACCOUNT_ACTIVATION_REQUIREMENT_SWITCH
)

# Grades download
GRADES_DOWNLOAD_ROUTING_KEY = config('GRADES_DOWNLOAD_ROUTING_KEY', default=HIGH_MEM_QUEUE)

GRADES_DOWNLOAD = config('GRADES_DOWNLOAD', default=GRADES_DOWNLOAD)

# financial reports
FINANCIAL_REPORTS = config('FINANCIAL_REPORTS', default=FINANCIAL_REPORTS)

##### ORA2 ######
# Prefix for uploads of example-based assessment AI classifiers
# This can be used to separate uploads for different environments
# within the same S3 bucket.
ORA2_FILE_PREFIX = config('ORA2_FILE_PREFIX', default=ORA2_FILE_PREFIX)

##### ACCOUNT LOCKOUT DEFAULT PARAMETERS #####
MAX_FAILED_LOGIN_ATTEMPTS_ALLOWED = config('MAX_FAILED_LOGIN_ATTEMPTS_ALLOWED', default=5)
MAX_FAILED_LOGIN_ATTEMPTS_LOCKOUT_PERIOD_SECS = config(
    'MAX_FAILED_LOGIN_ATTEMPTS_LOCKOUT_PERIOD_SECS',
    default=15 * 60
)

#### PASSWORD POLICY SETTINGS #####
PASSWORD_MIN_LENGTH = config('PASSWORD_MIN_LENGTH', default=PASSWORD_MIN_LENGTH)
PASSWORD_MAX_LENGTH = config('PASSWORD_MAX_LENGTH', default=PASSWORD_MIN_LENGTH)
PASSWORD_COMPLEXITY = config('PASSWORD_COMPLEXITY', default={})
PASSWORD_DICTIONARY_EDIT_DISTANCE_THRESHOLD = config(
    'PASSWORD_DICTIONARY_EDIT_DISTANCE_THRESHOLD',
    default='PASSWORD_DICTIONARY_EDIT_DISTANCE_THRESHOLD'
)
PASSWORD_DICTIONARY = config('PASSWORD_DICTIONARY', default=[])

### INACTIVITY SETTINGS ####
SESSION_INACTIVITY_TIMEOUT_IN_SECONDS = config(
    'SESSION_INACTIVITY_TIMEOUT_IN_SECONDS',
    default=None
)

##### LMS DEADLINE DISPLAY TIME_ZONE #######
TIME_ZONE_DISPLAYED_FOR_DEADLINES = config(
    'TIME_ZONE_DISPLAYED_FOR_DEADLINES',
    default=TIME_ZONE_DISPLAYED_FOR_DEADLINES
)

##### X-Frame-Options response header settings #####
X_FRAME_OPTIONS = config('X_FRAME_OPTIONS', default=X_FRAME_OPTIONS)

##### Third-party auth options ################################################
if FEATURES.get('ENABLE_THIRD_PARTY_AUTH'):
    AUTHENTICATION_BACKENDS = (
        config('THIRD_PARTY_AUTH_BACKENDS', default=[
            'social_core.backends.google.GoogleOAuth2',
            'social_core.backends.linkedin.LinkedinOAuth2',
            'social_core.backends.facebook.FacebookOAuth2',
            'social_core.backends.azuread.AzureADOAuth2',
            'third_party_auth.saml.SAMLAuthBackend',
            'third_party_auth.lti.LTIAuthBackend',
        ]) + list(AUTHENTICATION_BACKENDS)
    )

    # The reduced session expiry time during the third party login pipeline. (Value in seconds)
    SOCIAL_AUTH_PIPELINE_TIMEOUT = config('SOCIAL_AUTH_PIPELINE_TIMEOUT', default=600)

    # Most provider configuration is done via ConfigurationModels but for a few sensitive values
    # we allow configuration via credentials.vault.yaml instead (optionally).
    # The SAML private/public key values do not need the delimiter lines (such as
    # "-----BEGIN PRIVATE KEY-----", "-----END PRIVATE KEY-----" etc.) but they may be included
    # if you want (though it's easier to format the key values as JSON without the delimiters).
    SOCIAL_AUTH_SAML_SP_PRIVATE_KEY = config('SOCIAL_AUTH_SAML_SP_PRIVATE_KEY', default='')
    SOCIAL_AUTH_SAML_SP_PUBLIC_CERT = config('SOCIAL_AUTH_SAML_SP_PUBLIC_CERT', default='')
    SOCIAL_AUTH_OAUTH_SECRETS = config('SOCIAL_AUTH_OAUTH_SECRETS', default={})
    SOCIAL_AUTH_LTI_CONSUMER_SECRETS = config('SOCIAL_AUTH_LTI_CONSUMER_SECRETS', default={})

    # third_party_auth config moved to ConfigurationModels. This is for data migration only:
    THIRD_PARTY_AUTH_OLD_CONFIG = config('THIRD_PARTY_AUTH', default=None)

    if config('THIRD_PARTY_AUTH_SAML_FETCH_PERIOD_HOURS', default=24) is not None:
        CELERYBEAT_SCHEDULE['refresh-saml-metadata'] = {
            'task': 'third_party_auth.fetch_saml_metadata',
            'schedule': datetime.timedelta(hours=config(
                'THIRD_PARTY_AUTH_SAML_FETCH_PERIOD_HOURS',
                default=24
            )),
        }

    # The following can be used to integrate a custom login form with third_party_auth.
    # It should be a dict where the key is a word passed via ?auth_entry=, and the value is a
    # dict with an arbitrary 'secret_key' and a 'url'.
    THIRD_PARTY_AUTH_CUSTOM_AUTH_FORMS = config('THIRD_PARTY_AUTH_CUSTOM_AUTH_FORMS', default={})

##### OAUTH2 Provider ##############
if FEATURES.get('ENABLE_OAUTH2_PROVIDER'):
    OAUTH_OIDC_ISSUER = config('OAUTH_OIDC_ISSUER')
    OAUTH_ENFORCE_SECURE = config('OAUTH_ENFORCE_SECURE', default=True)
    OAUTH_ENFORCE_CLIENT_SECURE = config('OAUTH_ENFORCE_CLIENT_SECURE', default=True)
    # Defaults for the following are defined in lms.envs.common
    OAUTH_EXPIRE_DELTA = datetime.timedelta(
        days=config(
            'OAUTH_EXPIRE_CONFIDENTIAL_CLIENT_DAYS',
            default=OAUTH_EXPIRE_CONFIDENTIAL_CLIENT_DAYS
        )
    )
    OAUTH_EXPIRE_DELTA_PUBLIC = datetime.timedelta(
        days=config('OAUTH_EXPIRE_PUBLIC_CLIENT_DAYS', default=OAUTH_EXPIRE_PUBLIC_CLIENT_DAYS)
    )
    OAUTH_ID_TOKEN_EXPIRATION = config(
        'OAUTH_ID_TOKEN_EXPIRATION',
        default=OAUTH_ID_TOKEN_EXPIRATION
    )

##### ADVANCED_SECURITY_CONFIG #####
ADVANCED_SECURITY_CONFIG = config('ADVANCED_SECURITY_CONFIG', default={})

##### GOOGLE ANALYTICS IDS #####
GOOGLE_ANALYTICS_ACCOUNT = config('GOOGLE_ANALYTICS_ACCOUNT', default=None)
GOOGLE_ANALYTICS_LINKEDIN = config('GOOGLE_ANALYTICS_LINKEDIN', default=None)

##### OPTIMIZELY PROJECT ID #####
OPTIMIZELY_PROJECT_ID = config('OPTIMIZELY_PROJECT_ID', default=OPTIMIZELY_PROJECT_ID)

#### Course Registration Code length ####
REGISTRATION_CODE_LENGTH = config('REGISTRATION_CODE_LENGTH', default=8)

# REGISTRATION CODES DISPLAY INFORMATION
INVOICE_CORP_ADDRESS = config('INVOICE_CORP_ADDRESS', default=INVOICE_CORP_ADDRESS)
INVOICE_PAYMENT_INSTRUCTIONS = config(
    'INVOICE_PAYMENT_INSTRUCTIONS',
    default=INVOICE_PAYMENT_INSTRUCTIONS
)

# Which access.py permission names to check;
# We default this to the legacy permission 'see_exists'.
COURSE_CATALOG_VISIBILITY_PERMISSION = config(
    'COURSE_CATALOG_VISIBILITY_PERMISSION',
    default=COURSE_CATALOG_VISIBILITY_PERMISSION
)
COURSE_ABOUT_VISIBILITY_PERMISSION = config(
    'COURSE_ABOUT_VISIBILITY_PERMISSION',
    default=COURSE_ABOUT_VISIBILITY_PERMISSION
)


# Enrollment API Cache Timeout
ENROLLMENT_COURSE_DETAILS_CACHE_TIMEOUT = config(
    'ENROLLMENT_COURSE_DETAILS_CACHE_TIMEOUT',
    default=60
)

# PDF RECEIPT/INVOICE OVERRIDES
PDF_RECEIPT_TAX_ID = config('PDF_RECEIPT_TAX_ID', default=PDF_RECEIPT_TAX_ID)
PDF_RECEIPT_FOOTER_TEXT = config('PDF_RECEIPT_FOOTER_TEXT', default=PDF_RECEIPT_FOOTER_TEXT)
PDF_RECEIPT_DISCLAIMER_TEXT = config(
    'PDF_RECEIPT_DISCLAIMER_TEXT',
    default=PDF_RECEIPT_DISCLAIMER_TEXT
)
PDF_RECEIPT_BILLING_ADDRESS = config(
    'PDF_RECEIPT_BILLING_ADDRESS',
    default=PDF_RECEIPT_BILLING_ADDRESS
)
PDF_RECEIPT_TERMS_AND_CONDITIONS = config(
    'PDF_RECEIPT_TERMS_AND_CONDITIONS',
    default=PDF_RECEIPT_TERMS_AND_CONDITIONS)
PDF_RECEIPT_TAX_ID_LABEL = config('PDF_RECEIPT_TAX_ID_LABEL', default=PDF_RECEIPT_TAX_ID_LABEL)
PDF_RECEIPT_LOGO_PATH = config('PDF_RECEIPT_LOGO_PATH', default=PDF_RECEIPT_LOGO_PATH)
PDF_RECEIPT_COBRAND_LOGO_PATH = config(
    'PDF_RECEIPT_COBRAND_LOGO_PATH',
    default=PDF_RECEIPT_COBRAND_LOGO_PATH)
PDF_RECEIPT_LOGO_HEIGHT_MM = config(
    'PDF_RECEIPT_LOGO_HEIGHT_MM',
    default=PDF_RECEIPT_LOGO_HEIGHT_MM
)
PDF_RECEIPT_COBRAND_LOGO_HEIGHT_MM = config(
    'PDF_RECEIPT_COBRAND_LOGO_HEIGHT_MM', default=PDF_RECEIPT_COBRAND_LOGO_HEIGHT_MM
)

if FEATURES.get('ENABLE_COURSEWARE_SEARCH') or \
   FEATURES.get('ENABLE_DASHBOARD_SEARCH') or \
   FEATURES.get('ENABLE_COURSE_DISCOVERY') or \
   FEATURES.get('ENABLE_TEAMS'):
    # Use ElasticSearch as the search engine herein
    SEARCH_ENGINE = "search.elastic.ElasticSearchEngine"

ELASTIC_SEARCH_CONFIG = config('ELASTIC_SEARCH_CONFIG', default=[{}])

# Facebook app
FACEBOOK_API_VERSION = config("FACEBOOK_API_VERSION", default=None)
FACEBOOK_APP_SECRET = config("FACEBOOK_APP_SECRET", default='ThisIsAnExampleKeyForDevPurposeOnly')
FACEBOOK_APP_ID = config("FACEBOOK_APP_ID", default=None)

XBLOCK_SETTINGS = config('XBLOCK_SETTINGS', default={})
XBLOCK_SETTINGS.setdefault("VideoDescriptor", {})["licensing_enabled"] = FEATURES.get(
    'LICENSING',
    False
)
XBLOCK_SETTINGS.setdefault("VideoModule", {})['YOUTUBE_API_KEY'] = config(
    'YOUTUBE_API_KEY',
    default=YOUTUBE_API_KEY
)

##### CDN EXPERIMENT/MONITORING FLAGS #####
CDN_VIDEO_URLS = config('CDN_VIDEO_URLS', default=CDN_VIDEO_URLS)
ONLOAD_BEACON_SAMPLE_RATE = config('ONLOAD_BEACON_SAMPLE_RATE', default=ONLOAD_BEACON_SAMPLE_RATE)

##### ECOMMERCE API CONFIGURATION SETTINGS #####
ECOMMERCE_PUBLIC_URL_ROOT = config('ECOMMERCE_PUBLIC_URL_ROOT', default=ECOMMERCE_PUBLIC_URL_ROOT)
ECOMMERCE_API_URL = config('ECOMMERCE_API_URL', default=ECOMMERCE_API_URL)
ECOMMERCE_API_TIMEOUT = config('ECOMMERCE_API_TIMEOUT', default=ECOMMERCE_API_TIMEOUT)

COURSE_CATALOG_API_URL = config('COURSE_CATALOG_API_URL', default=COURSE_CATALOG_API_URL)

CREDENTIALS_INTERNAL_SERVICE_URL = config(
    'CREDENTIALS_INTERNAL_SERVICE_URL',
    default=CREDENTIALS_INTERNAL_SERVICE_URL)
CREDENTIALS_PUBLIC_SERVICE_URL = config(
    'CREDENTIALS_PUBLIC_SERVICE_URL',
    default=CREDENTIALS_PUBLIC_SERVICE_URL)

##### Custom Courses for EdX #####
if FEATURES.get('CUSTOM_COURSES_EDX'):
    INSTALLED_APPS += ('lms.djangoapps.ccx', 'openedx.core.djangoapps.ccxcon')
    MODULESTORE_FIELD_OVERRIDE_PROVIDERS += (
        'lms.djangoapps.ccx.overrides.CustomCoursesForEdxOverrideProvider',
    )
CCX_MAX_STUDENTS_ALLOWED = config('CCX_MAX_STUDENTS_ALLOWED', default=CCX_MAX_STUDENTS_ALLOWED)

##### Individual Due Date Extensions #####
if FEATURES.get('INDIVIDUAL_DUE_DATES'):
    FIELD_OVERRIDE_PROVIDERS += (
        'courseware.student_field_overrides.IndividualStudentOverrideProvider',
    )

##### Self-Paced Course Due Dates #####
XBLOCK_FIELD_DATA_WRAPPERS += (
    'lms.djangoapps.courseware.field_overrides:OverrideModulestoreFieldData.wrap',
)

MODULESTORE_FIELD_OVERRIDE_PROVIDERS += (
    'courseware.self_paced_overrides.SelfPacedDateOverrideProvider',
)

# PROFILE IMAGE CONFIG
PROFILE_IMAGE_BACKEND = config('PROFILE_IMAGE_BACKEND', default=PROFILE_IMAGE_BACKEND)
PROFILE_IMAGE_SECRET_KEY = config('PROFILE_IMAGE_SECRET_KEY', default=PROFILE_IMAGE_SECRET_KEY)
PROFILE_IMAGE_MAX_BYTES = config('PROFILE_IMAGE_MAX_BYTES', default=PROFILE_IMAGE_MAX_BYTES)
PROFILE_IMAGE_MIN_BYTES = config('PROFILE_IMAGE_MIN_BYTES', default=PROFILE_IMAGE_MIN_BYTES)
PROFILE_IMAGE_DEFAULT_FILENAME = 'images/profiles/default'

# EdxNotes config

EDXNOTES_PUBLIC_API = config('EDXNOTES_PUBLIC_API', default=EDXNOTES_PUBLIC_API)
EDXNOTES_INTERNAL_API = config('EDXNOTES_INTERNAL_API', default=EDXNOTES_INTERNAL_API)

EDXNOTES_CONNECT_TIMEOUT = config('EDXNOTES_CONNECT_TIMEOUT', default=EDXNOTES_CONNECT_TIMEOUT)
EDXNOTES_READ_TIMEOUT = config('EDXNOTES_READ_TIMEOUT', default=EDXNOTES_READ_TIMEOUT)

##### Credit Provider Integration #####

CREDIT_PROVIDER_SECRET_KEYS = config("CREDIT_PROVIDER_SECRET_KEYS", default={})

##################### LTI Provider #####################
if FEATURES.get('ENABLE_LTI_PROVIDER'):
    INSTALLED_APPS += ('lti_provider',)
    AUTHENTICATION_BACKENDS += ('lti_provider.users.LtiBackend', )

LTI_USER_EMAIL_DOMAIN = config('LTI_USER_EMAIL_DOMAIN', default='lti.example.com')

# For more info on this, see the notes in common.py
LTI_AGGREGATE_SCORE_PASSBACK_DELAY = config(
    'LTI_AGGREGATE_SCORE_PASSBACK_DELAY',
    default=LTI_AGGREGATE_SCORE_PASSBACK_DELAY
)

##################### Credit Provider help link ####################
CREDIT_HELP_LINK_URL = config('CREDIT_HELP_LINK_URL', default=CREDIT_HELP_LINK_URL)

#### JWT configuration ####
JWT_AUTH.update(config('JWT_AUTH', default={}))
JWT_PRIVATE_SIGNING_KEY = config('JWT_PRIVATE_SIGNING_KEY', default=JWT_PRIVATE_SIGNING_KEY)
JWT_EXPIRED_PRIVATE_SIGNING_KEYS = config(
    'JWT_EXPIRED_PRIVATE_SIGNING_KEYS',
    default=JWT_EXPIRED_PRIVATE_SIGNING_KEYS
)

################# PROCTORING CONFIGURATION ##################

PROCTORING_BACKEND_PROVIDER = config(
    'PROCTORING_BACKEND_PROVIDER',
    default=PROCTORING_BACKEND_PROVIDER
)
PROCTORING_SETTINGS = config("PROCTORING_SETTINGS", default=PROCTORING_SETTINGS)

################# MICROSITE ####################
MICROSITE_CONFIGURATION = config('MICROSITE_CONFIGURATION', default={})
MICROSITE_ROOT_DIR = path(config('MICROSITE_ROOT_DIR', default=''))
# this setting specify which backend to be used when pulling microsite specific configuration
MICROSITE_BACKEND = config('MICROSITE_BACKEND', default=MICROSITE_BACKEND)
# this setting specify which backend to be used when loading microsite specific templates
MICROSITE_TEMPLATE_BACKEND = config(
    'MICROSITE_TEMPLATE_BACKEND',
    default=MICROSITE_TEMPLATE_BACKEND
)
# TTL for microsite database template cache
MICROSITE_DATABASE_TEMPLATE_CACHE_TTL = config(
    'MICROSITE_DATABASE_TEMPLATE_CACHE_TTL',
    default=MICROSITE_DATABASE_TEMPLATE_CACHE_TTL
)

# Course Content Bookmarks Settings
MAX_BOOKMARKS_PER_COURSE = config(
    'MAX_BOOKMARKS_PER_COURSE',
    default=MAX_BOOKMARKS_PER_COURSE
)

# Offset for pk of courseware.StudentModuleHistoryExtended
STUDENTMODULEHISTORYEXTENDED_OFFSET = config(
    'STUDENTMODULEHISTORYEXTENDED_OFFSET',
    default=STUDENTMODULEHISTORYEXTENDED_OFFSET
)

# Cutoff date for granting audit certificates
if config('AUDIT_CERT_CUTOFF_DATE', default=None):
    AUDIT_CERT_CUTOFF_DATE = dateutil.parser.parse(config('AUDIT_CERT_CUTOFF_DATE'))

################################ Settings for Credentials Service ################################

CREDENTIALS_GENERATION_ROUTING_KEY = config(
    'CREDENTIALS_GENERATION_ROUTING_KEY',
    default=HIGH_PRIORITY_QUEUE
)

# The extended StudentModule history table
if FEATURES.get('ENABLE_CSMH_EXTENDED'):
    INSTALLED_APPS += ('coursewarehistoryextended',)

API_ACCESS_MANAGER_EMAIL = config(
    'API_ACCESS_MANAGER_EMAIL',
    default=API_ACCESS_MANAGER_EMAIL)
API_ACCESS_FROM_EMAIL = config(
    'API_ACCESS_FROM_EMAIL',
    default=API_ACCESS_FROM_EMAIL)

# Mobile App Version Upgrade config
APP_UPGRADE_CACHE_TIMEOUT = config(
    'APP_UPGRADE_CACHE_TIMEOUT',
    default=APP_UPGRADE_CACHE_TIMEOUT
)

AFFILIATE_COOKIE_NAME = config(
    'AFFILIATE_COOKIE_NAME',
    default=AFFILIATE_COOKIE_NAME
)

############## Settings for LMS Context Sensitive Help ##############

HELP_TOKENS_BOOKS = config('HELP_TOKENS_BOOKS', default=HELP_TOKENS_BOOKS)


############## OPEN EDX ENTERPRISE SERVICE CONFIGURATION ######################
# The Open edX Enterprise service is currently hosted via the LMS container/process.
# However, for all intents and purposes this service is treated as a standalone IDA.
# These configuration settings are specific to the Enterprise service and you should
# not find references to them within the edx-platform project.

# Publicly-accessible enrollment URL, for use on the client side.
ENTERPRISE_PUBLIC_ENROLLMENT_API_URL = config(
    'ENTERPRISE_PUBLIC_ENROLLMENT_API_URL',
    default=(LMS_ROOT_URL or '') + '/api/enrollment/v1/'
)

# Enrollment URL used on the server-side.
ENTERPRISE_ENROLLMENT_API_URL = config(
    'ENTERPRISE_ENROLLMENT_API_URL',
    default=ENTERPRISE_ENROLLMENT_API_URL
)

# Enterprise logo image size limit in KB's
ENTERPRISE_CUSTOMER_LOGO_IMAGE_SIZE = config(
    'ENTERPRISE_CUSTOMER_LOGO_IMAGE_SIZE',
    default=ENTERPRISE_CUSTOMER_LOGO_IMAGE_SIZE
)

# Course enrollment modes to be hidden in the Enterprise enrollment page
# if the "Hide audit track" flag is enabled for an EnterpriseCustomer
ENTERPRISE_COURSE_ENROLLMENT_AUDIT_MODES = config(
    'ENTERPRISE_COURSE_ENROLLMENT_AUDIT_MODES',
    default=ENTERPRISE_COURSE_ENROLLMENT_AUDIT_MODES
)


############## ENTERPRISE SERVICE API CLIENT CONFIGURATION ######################
# The LMS communicates with the Enterprise service via the EdxRestApiClient class
# The below environmental settings are utilized by the LMS when interacting with
# the service, and override the default parameters which are defined in common.py

DEFAULT_ENTERPRISE_API_URL = None
if LMS_ROOT_URL is not None:
    DEFAULT_ENTERPRISE_API_URL = LMS_ROOT_URL + '/enterprise/api/v1/'
ENTERPRISE_API_URL = config('ENTERPRISE_API_URL', default=DEFAULT_ENTERPRISE_API_URL)

ENTERPRISE_SERVICE_WORKER_USERNAME = config(
    'ENTERPRISE_SERVICE_WORKER_USERNAME',
    default=ENTERPRISE_SERVICE_WORKER_USERNAME
)
ENTERPRISE_API_CACHE_TIMEOUT = config(
    'ENTERPRISE_API_CACHE_TIMEOUT',
    default=ENTERPRISE_API_CACHE_TIMEOUT
)

############## ENTERPRISE SERVICE LMS CONFIGURATION ##################################
# The LMS has some features embedded that are related to the Enterprise service, but
# which are not provided by the Enterprise service. These settings override the
# base values for the parameters as defined in common.py

ENTERPRISE_PLATFORM_WELCOME_TEMPLATE = config(
    'ENTERPRISE_PLATFORM_WELCOME_TEMPLATE',
    default=ENTERPRISE_PLATFORM_WELCOME_TEMPLATE
)
ENTERPRISE_SPECIFIC_BRANDED_WELCOME_TEMPLATE = config(
    'ENTERPRISE_SPECIFIC_BRANDED_WELCOME_TEMPLATE',
    default=ENTERPRISE_SPECIFIC_BRANDED_WELCOME_TEMPLATE
)
ENTERPRISE_EXCLUDED_REGISTRATION_FIELDS = set(
    config(
        'ENTERPRISE_EXCLUDED_REGISTRATION_FIELDS',
        default=ENTERPRISE_EXCLUDED_REGISTRATION_FIELDS
    )
)

############## CATALOG/DISCOVERY SERVICE API CLIENT CONFIGURATION ######################
# The LMS communicates with the Catalog service via the EdxRestApiClient class
# The below environmental settings are utilized by the LMS when interacting with
# the service, and override the default parameters which are defined in common.py

COURSES_API_CACHE_TIMEOUT = config('COURSES_API_CACHE_TIMEOUT', default=COURSES_API_CACHE_TIMEOUT)

# Add an ICP license for serving content in China if your organization is registered to do so
ICP_LICENSE = config('ICP_LICENSE', default=None)

############## Settings for CourseGraph ############################
COURSEGRAPH_JOB_QUEUE = config('COURSEGRAPH_JOB_QUEUE', default=LOW_PRIORITY_QUEUE)
