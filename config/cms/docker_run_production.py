"""
This is the settings to run the Open edX CMS with Docker the FUN way.
"""

import os
import platform

from lms.envs.fun.utils import Configuration
from path import Path as path
from xmodule.modulestore.modulestore_settings import convert_module_store_setting_if_needed

from ..common import *


# Load custom configuration parameters from yaml files
config = Configuration(os.path.dirname(__file__))

############### ALWAYS THE SAME ################################

DEBUG = False

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
    "DEFAULT_PRIORITY_QUEUE", default="edx.cms.core.default")
HIGH_PRIORITY_QUEUE = config(
    "HIGH_PRIORITY_QUEUE", default="edx.cms.core.high")
LOW_PRIORITY_QUEUE = config(
    "LOW_PRIORITY_QUEUE", default="edx.cms.core.low")

CELERY_QUEUES = config("CELERY_QUEUES", default={
    DEFAULT_PRIORITY_QUEUE: {},
    HIGH_PRIORITY_QUEUE: {},
    LOW_PRIORITY_QUEUE: {}
})

CELERY_ROUTES = 'cms.celery.Router'

# Force accepted content to "json" only. If we also accept pickle-serialized
# messages, the worker will crash when it's running with a privileged user (even
# if it's not the root user but a user belonging to the root group, which is our
# case with OpenShift).
CELERY_ACCEPT_CONTENT = ['json']

############# NON-SECURE ENV CONFIG ##############################
# Things like server locations, ports, etc.

# DEFAULT_COURSE_ABOUT_IMAGE_URL specifies the default image to show for courses that don't
# provide one
DEFAULT_COURSE_ABOUT_IMAGE_URL = config(
    'DEFAULT_COURSE_ABOUT_IMAGE_URL',
    default=DEFAULT_COURSE_ABOUT_IMAGE_URL)

# GITHUB_REPO_ROOT is the base directory
# for course data
GITHUB_REPO_ROOT = config('GITHUB_REPO_ROOT', default=GITHUB_REPO_ROOT)

STATIC_URL = '/static/'
STATIC_ROOT = path('/edx/app/edxapp/staticfiles')

WEBPACK_LOADER['DEFAULT']['STATS_FILE'] = STATIC_ROOT / 'webpack-stats.json'

EMAIL_BACKEND = config('EMAIL_BACKEND', default=EMAIL_BACKEND)
EMAIL_FILE_PATH = config('EMAIL_FILE_PATH', default=None)

EMAIL_HOST = config('EMAIL_HOST', default=EMAIL_HOST)
EMAIL_PORT = config('EMAIL_PORT', default=EMAIL_PORT)
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=EMAIL_USE_TLS)

LMS_BASE = config('LMS_BASE', default='localhost:8072')
CMS_BASE = config('CMS_BASE', default='localhost:8082')

LMS_ROOT_URL = config('LMS_ROOT_URL', default='http://localhost:8072')

SITE_NAME = config('SITE_NAME', default=SITE_NAME)

ALLOWED_HOSTS = [CMS_BASE.split(':')[0]]

LOG_DIR = config('LOG_DIR', default='/edx/var/logs/edx')

CACHES = config('CACHES', default={
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
})

SESSION_COOKIE_DOMAIN = config('SESSION_COOKIE_DOMAIN', default=None)
SESSION_COOKIE_HTTPONLY = config('SESSION_COOKIE_HTTPONLY', default=True)
SESSION_ENGINE = config(
    'SESSION_ENGINE', default='django.contrib.sessions.backends.cache')
SESSION_COOKIE_SECURE = config(
    'SESSION_COOKIE_SECURE', default=SESSION_COOKIE_SECURE)
SESSION_SAVE_EVERY_REQUEST = config(
    'SESSION_SAVE_EVERY_REQUEST',
    default=SESSION_SAVE_EVERY_REQUEST)

# social sharing settings
SOCIAL_SHARING_SETTINGS = config(
    'SOCIAL_SHARING_SETTINGS', default=SOCIAL_SHARING_SETTINGS)

REGISTRATION_EMAIL_PATTERNS_ALLOWED = config(
    'REGISTRATION_EMAIL_PATTERNS_ALLOWED', default=None)

# allow for environments to specify what cookie name our login subsystem should use
# this is to fix a bug regarding simultaneous logins between edx.org and edge.edx.org which can
# happen with some browsers (e.g. Firefox)
if config('SESSION_COOKIE_NAME', default=None):
    # NOTE, there's a bug in Django (http://bugs.python.org/issue18012) which necessitates this
    # being a str()
    SESSION_COOKIE_NAME = str(config('SESSION_COOKIE_NAME'))

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

# Determines whether the CSRF token can be transported on
# unencrypted channels. It is set to False here for backward compatibility,
# but it is highly recommended that this is True for environments accessed
# by end users.
CSRF_COOKIE_SECURE = config('CSRF_COOKIE_SECURE', default=False)

# Email overrides
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default=DEFAULT_FROM_EMAIL)
DEFAULT_FEEDBACK_EMAIL = config(
    'DEFAULT_FEEDBACK_EMAIL', default=DEFAULT_FEEDBACK_EMAIL)
ADMINS = config('ADMINS', default=ADMINS)
SERVER_EMAIL = config('SERVER_EMAIL', default=SERVER_EMAIL)
MKTG_URLS = config('MKTG_URLS', default=MKTG_URLS)
TECH_SUPPORT_EMAIL = config('TECH_SUPPORT_EMAIL', default=TECH_SUPPORT_EMAIL)

for name, value in config('CODE_JAIL', default={}).items():
    oldvalue = CODE_JAIL.get(name)
    if isinstance(oldvalue, dict):
        for subname, subvalue in value.items():
            oldvalue[subname] = subvalue
    else:
        CODE_JAIL[name] = value

COURSES_WITH_UNSAFE_CODE = config('COURSES_WITH_UNSAFE_CODE', default=[])

ASSET_IGNORE_REGEX = config('ASSET_IGNORE_REGEX', default=ASSET_IGNORE_REGEX)

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
    'COMPREHENSIVE_THEME_LOCALE_PATHS', default=[])

DEFAULT_SITE_THEME = config('DEFAULT_SITE_THEME', default=DEFAULT_SITE_THEME)
ENABLE_COMPREHENSIVE_THEMING = config(
    'ENABLE_COMPREHENSIVE_THEMING',
    default=ENABLE_COMPREHENSIVE_THEMING
)

# Timezone overrides
TIME_ZONE = config('TIME_ZONE', default=TIME_ZONE)

# Push to LMS overrides
GIT_REPO_EXPORT_DIR = config(
    'GIT_REPO_EXPORT_DIR', default='/edx/var/edxapp/export_course_repos')

# Translation overrides
LANGUAGES = config('LANGUAGES', default=LANGUAGES)
LANGUAGE_CODE = config('LANGUAGE_CODE', default=LANGUAGE_CODE)
LANGUAGE_COOKIE = config('LANGUAGE_COOKIE', default=LANGUAGE_COOKIE)

USE_I18N = config('USE_I18N', default=USE_I18N)

# Override feature by feature by whatever is being redefined in the settings.yaml file
CONFIG_FEATURES = config('FEATURES', default={})
FEATURES.update(CONFIG_FEATURES)


# Additional installed apps
for app in config('ADDL_INSTALLED_APPS', default=[]):
    INSTALLED_APPS += (app,)

WIKI_ENABLED = config('WIKI_ENABLED', default=WIKI_ENABLED)

# Configure Logging

# Default format for syslog logging
standard_format = (
    '%(asctime)s %(levelname)s %(process)d [%(name)s] %(filename)s:%(lineno)d - %(message)s'
)
syslog_format = (
    '[variant:cms][%(name)s][env:sandbox] %(levelname)s '
    '[{hostname}  %(process)d] [%(filename)s:%(lineno)d] - %(message)s'
).format(hostname=platform.node().split('.')[0])

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

# theming start:
PLATFORM_NAME = config('PLATFORM_NAME', default=PLATFORM_NAME)
STUDIO_NAME = config('STUDIO_NAME', default='Open edX Studio')
STUDIO_SHORT_NAME = config('STUDIO_SHORT_NAME', default='Studio')

# Event Tracking
TRACKING_IGNORE_URL_PATTERNS = config(
    'TRACKING_IGNORE_URL_PATTERNS',
    default=None
)

# Django CAS external authentication settings
CAS_EXTRA_LOGIN_PARAMS = config('CAS_EXTRA_LOGIN_PARAMS', default=None)
if FEATURES.get('AUTH_USE_CAS'):
    CAS_SERVER_URL = config('CAS_SERVER_URL', default=None)
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

# Specific setting for the File Upload Service to store media in a bucket.
FILE_UPLOAD_STORAGE_BUCKET_NAME = config(
    'FILE_UPLOAD_STORAGE_BUCKET_NAME',
    default=FILE_UPLOAD_STORAGE_BUCKET_NAME
)
FILE_UPLOAD_STORAGE_PREFIX = config(
    'FILE_UPLOAD_STORAGE_PREFIX',
    default=FILE_UPLOAD_STORAGE_PREFIX
)

################ SECURE AUTH ITEMS ###############################

############### XBlock filesystem field config ##########
DJFS = config('DJFS', default=None)

EMAIL_HOST_USER = config('EMAIL_HOST_USER', default=EMAIL_HOST_USER)
EMAIL_HOST_PASSWORD = config(
    'EMAIL_HOST_PASSWORD', default=EMAIL_HOST_PASSWORD)

# Note that this is the Studio key for Segment. There is a separate key for the LMS.
CMS_SEGMENT_KEY = config('SEGMENT_KEY', default=None)

SECRET_KEY = config(
    'SECRET_KEY', default='ThisIsAnExampleKeyForDevPurposeOnly')

DEFAULT_FILE_STORAGE = config(
    'DEFAULT_FILE_STORAGE',
    default='django.core.files.storage.FileSystemStorage'
)

USER_TASKS_ARTIFACT_STORAGE = COURSE_IMPORT_EXPORT_STORAGE

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

# Configure the MODULESTORE
MODULESTORE = convert_module_store_setting_if_needed(
    config('MODULESTORE', default=MODULESTORE))

DOC_STORE_CONFIG = config('DOC_STORE_CONFIG', default={
    'db': 'edxapp',
    'host': 'mongodb',
})

MODULESTORE_FIELD_OVERRIDE_PROVIDERS = config(
    'MODULESTORE_FIELD_OVERRIDE_PROVIDERS',
    default=MODULESTORE_FIELD_OVERRIDE_PROVIDERS
)

XBLOCK_FIELD_DATA_WRAPPERS = config(
    'XBLOCK_FIELD_DATA_WRAPPERS',
    default=XBLOCK_FIELD_DATA_WRAPPERS
)

CONTENTSTORE = config('CONTENTSTORE', default={
    'DOC_STORE_CONFIG': {
        'host': ['mongodb'],
        'db': 'edxapp',
        'port': 27017
    },
    'ENGINE': 'xmodule.contentstore.mongo.MongoContentStore',
})

update_module_store_settings(MODULESTORE, doc_store_settings=DOC_STORE_CONFIG)

# Datadog for events!
DATADOG = config('DATADOG', default={})
DATADOG.update(config('DATADOG', default={}))

# TODO: deprecated (compatibility with previous settings)
DATADOG['api_key'] = config('DATADOG_API', default=None)

# Celery Broker
CELERY_ALWAYS_EAGER = config('CELERY_ALWAYS_EAGER', default=False)
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

# Message expiry time in seconds
CELERY_EVENT_QUEUE_TTL = config('CELERY_EVENT_QUEUE_TTL', default=None)

# Event tracking
TRACKING_BACKENDS.update(config('TRACKING_BACKENDS', default={}))
EVENT_TRACKING_BACKENDS['tracking_logs']['OPTIONS']['backends'].update(config(
    'EVENT_TRACKING_BACKENDS',
    default={})
)
EVENT_TRACKING_BACKENDS['segmentio']['OPTIONS']['processors'][0]['OPTIONS']['whitelist'].extend(
    config('EVENT_TRACKING_SEGMENTIO_EMIT_WHITELIST', default=[]))

VIRTUAL_UNIVERSITIES = config('VIRTUAL_UNIVERSITIES', default=[])

##### ACCOUNT LOCKOUT DEFAULT PARAMETERS #####
MAX_FAILED_LOGIN_ATTEMPTS_ALLOWED = config(
    'MAX_FAILED_LOGIN_ATTEMPTS_ALLOWED', default=5)
MAX_FAILED_LOGIN_ATTEMPTS_LOCKOUT_PERIOD_SECS = config(
    'MAX_FAILED_LOGIN_ATTEMPTS_LOCKOUT_PERIOD_SECS',
    default=15 * 60
)

#### PASSWORD POLICY SETTINGS #####
PASSWORD_MIN_LENGTH = config(
    'PASSWORD_MIN_LENGTH', default=PASSWORD_MIN_LENGTH)
PASSWORD_MAX_LENGTH = config(
    'PASSWORD_MAX_LENGTH', default=PASSWORD_MIN_LENGTH)
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

##### X-Frame-Options response header settings #####
X_FRAME_OPTIONS = config('X_FRAME_OPTIONS', default=X_FRAME_OPTIONS)

##### ADVANCED_SECURITY_CONFIG #####
ADVANCED_SECURITY_CONFIG = config('ADVANCED_SECURITY_CONFIG', default={})

################ ADVANCED COMPONENT/PROBLEM TYPES ###############

ADVANCED_PROBLEM_TYPES = config(
    'ADVANCED_PROBLEM_TYPES', default=ADVANCED_PROBLEM_TYPES)

################ VIDEO UPLOAD PIPELINE ###############

VIDEO_UPLOAD_PIPELINE = config(
    'VIDEO_UPLOAD_PIPELINE', default=VIDEO_UPLOAD_PIPELINE)

################ PUSH NOTIFICATIONS ###############

PARSE_KEYS = config('PARSE_KEYS', default={})


# Video Caching. Pairing country codes with CDN URLs.
# Example: {'CN': 'http://api.xuetangx.com/edx/video?s3_url='}
VIDEO_CDN_URL = config('VIDEO_CDN_URL', default={})

if FEATURES['ENABLE_COURSEWARE_INDEX'] or FEATURES['ENABLE_LIBRARY_INDEX']:
    # Use ElasticSearch for the search engine
    SEARCH_ENGINE = 'search.elastic.ElasticSearchEngine'

ELASTIC_SEARCH_CONFIG = config('ELASTIC_SEARCH_CONFIG', default=[{}])

XBLOCK_SETTINGS = config('XBLOCK_SETTINGS', default={})
XBLOCK_SETTINGS.setdefault('VideoDescriptor', {})['licensing_enabled'] = FEATURES.get(
    'LICENSING',
    False
)
XBLOCK_SETTINGS.setdefault('VideoModule', {})['YOUTUBE_API_KEY'] = config(
    'YOUTUBE_API_KEY',
    default=YOUTUBE_API_KEY)

################# PROCTORING CONFIGURATION ##################

PROCTORING_BACKEND_PROVIDER = config(
    'PROCTORING_BACKEND_PROVIDER',
    default=PROCTORING_BACKEND_PROVIDER
)
PROCTORING_SETTINGS = config(
    'PROCTORING_SETTINGS', default=PROCTORING_SETTINGS)

################# MICROSITE ####################
# microsite specific configurations.
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

############################ OAUTH2 Provider ###################################

# OpenID Connect issuer ID. Normally the URL of the authentication endpoint.
OAUTH_OIDC_ISSUER = config('OAUTH_OIDC_ISSUER', default=None)

#### JWT configuration ####
JWT_AUTH.update(config('JWT_AUTH', default={}))

######################## CUSTOM COURSES for EDX CONNECTOR ######################
if FEATURES.get('CUSTOM_COURSES_EDX'):
    INSTALLED_APPS += ('openedx.core.djangoapps.ccxcon',)

# Partner support link for CMS footer
PARTNER_SUPPORT_EMAIL = config(
    'PARTNER_SUPPORT_EMAIL', default=PARTNER_SUPPORT_EMAIL)

# Affiliate cookie tracking
AFFILIATE_COOKIE_NAME = config(
    'AFFILIATE_COOKIE_NAME', default=AFFILIATE_COOKIE_NAME)

############## Settings for Studio Context Sensitive Help ##############

HELP_TOKENS_BOOKS = config('HELP_TOKENS_BOOKS', default=HELP_TOKENS_BOOKS)

############## Settings for CourseGraph ############################
COURSEGRAPH_JOB_QUEUE = config(
    'COURSEGRAPH_JOB_QUEUE', default=LOW_PRIORITY_QUEUE)
