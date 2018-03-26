# -*- coding: utf-8 -*-


# FUN_BASE_ROOT should be added to Python PATH before importing this file
import os
import sys
from path import path

BASE_ROOT = path('/edx/app/edxapp/')
BASE_DATA = path('/edx/var/edxapp/')

FUN_BASE_ROOT = BASE_ROOT / 'fun-apps'
DATA_DIR = BASE_ROOT / 'data'

sys.path.append(FUN_BASE_ROOT)

os.environ['BASE_ROOT'] = BASE_ROOT
os.environ['CONFIG_ROOT'] = BASE_ROOT
os.environ['SERVICE_VARIANT'] = 'lms'
os.environ['SHARED_ROOT'] = BASE_DATA / 'shared'

os.environ['STATIC_ROOT_BASE'] = '/edx/var/edxapp/static'
os.environ['STATIC_ROOT'] = '/edx/var/edxapp/static/lms'
os.environ['STATIC_URL'] = '/static/'

os.environ['MEDIA_ROOT'] = '/edx/var/edxapp/media'
os.environ['MEDIA_URL'] = '/media/'



HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'courses.search_indexes.ConfigurableElasticSearchEngine',
        'URL': 'http://localhost:9200/',
        'INDEX_NAME': 'haystack',
    },
}

BROKER_URL = 'amqp://guest@rabbitmq:5672'
MEMCACHED_URL = 'memcached:11211'


from lms.envs.common import *  # pylint: disable=wildcard-import, unused-wildcard-import

from .docker_run_common import *  # pylint: disable=wildcard-import, unused-wildcard-import

################################## from lms.auth.json #############################################

DATABASES = {
        "default": {
          "ENGINE": "django.db.backends.mysql",
          "HOST": "mysql",
          "NAME": "edxapp",
          "PASSWORD": "password",
          "PORT": "3306",
          "USER": "fun"
        },
        "read_replica": {
          "ENGINE": "django.db.backends.mysql",
          "HOST": "mysql",
          "NAME": "edxapp",
          "PASSWORD": "password",
          "PORT": "3306",
          "USER": "fun"
        }
}

DOC_STORE_CONFIG = {
        "collection": "modulestore",
        "db": "edxapp",
        "host": [
          "mongodb"
        ]
}

MODULESTORE = {
      "default": {
        "ENGINE": "xmodule.modulestore.mixed.MixedModuleStore",
        "OPTIONS": {
          "mappings": {},
          "stores": [
            {
              "DOC_STORE_CONFIG": {
                "collection": "modulestore",
                "db": "edxapp",
                "host": [
                  "mongodb"
                ]
              },
              "ENGINE": "xmodule.modulestore.mongo.DraftMongoModuleStore",
              "NAME": "draft",
              "OPTIONS": {
                "default_class": "xmodule.hidden_module.HiddenDescriptor",
                "fs_root": "/data/data",
                "render_template": "edxmako.shortcuts.render_to_string"
              }
            },
            {
              "ENGINE": "xmodule.modulestore.xml.XMLModuleStore",
              "NAME": "xml",
              "OPTIONS": {
                "data_dir": "/data/data",
                "default_class": "xmodule.hidden_module.HiddenDescriptor"
              }
            },
            {
              "DOC_STORE_CONFIG": {
                "collection": "modulestore",
                "db": "edxapp",
                "host": [
                  "mongodb"
                ]
              },
              "ENGINE": "xmodule.modulestore.split_mongo.split_draft.DraftVersioningModuleStore",
              "NAME": "split",
              "OPTIONS": {
                "default_class": "xmodule.hidden_module.HiddenDescriptor",
                "fs_root": "/data/data",
                "render_template": "edxmako.shortcuts.render_to_string"
              }
            }
          ]
        }
      }
}

CONTENTSTORE = {
    "ADDITIONAL_OPTIONS": {},
    "DOC_STORE_CONFIG": {
      "collection": "modulestore",
      "db": "edxapp",
      "host": [
        "mongodb"
      ]
    },
    "ENGINE": "xmodule.contentstore.mongo.MongoContentStore",
    "OPTIONS": {
      "db": "edxapp",
      "host": [
        "mongodb"
      ]
    }
}


XQUEUE_INTERFACE = {
      "basic_auth": [
        "edx",
        "edx"
      ],
      "django_auth": {
        "password": "password",
        "username": "lms"
      },
      "url": "http://localhost:18040"
}



################################## from lms/envs/aws.py ###########################################

# SERVICE_VARIANT specifies name of the variant used, which decides what JSON
# configuration files are read during startup.
SERVICE_VARIANT = os.environ.get('SERVICE_VARIANT', None)


from openedx.core.lib.logsettings import get_logger_config

LOGGING = get_logger_config(LOG_DIR,
                            logging_env='sandbox',
                            debug=False,
                            service_variant=SERVICE_VARIANT)

from xmodule.modulestore.modulestore_settings import convert_module_store_setting_if_needed


# CONFIG_PREFIX specifies the prefix of the JSON configuration files,
# based on the service variant. If no variant is use, don't use a
# prefix.
CONFIG_PREFIX = SERVICE_VARIANT + "." if SERVICE_VARIANT else ""

################################ ALWAYS THE SAME ##############################

SESSION_ENGINE = 'django.contrib.sessions.backends.cache'

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

# Rename the exchange and queues for each variant
QUEUE_VARIANT = CONFIG_PREFIX.lower()

CELERY_DEFAULT_EXCHANGE = 'edx.{0}core'.format(QUEUE_VARIANT)

HIGH_PRIORITY_QUEUE = 'edx.{0}core.high'.format(QUEUE_VARIANT)
DEFAULT_PRIORITY_QUEUE = 'edx.{0}core.default'.format(QUEUE_VARIANT)
LOW_PRIORITY_QUEUE = 'edx.{0}core.low'.format(QUEUE_VARIANT)
HIGH_MEM_QUEUE = 'edx.{0}core.high_mem'.format(QUEUE_VARIANT)

CELERY_DEFAULT_QUEUE = DEFAULT_PRIORITY_QUEUE
CELERY_DEFAULT_ROUTING_KEY = DEFAULT_PRIORITY_QUEUE

CELERY_QUEUES = {
    HIGH_PRIORITY_QUEUE: {},
    LOW_PRIORITY_QUEUE: {},
    DEFAULT_PRIORITY_QUEUE: {},
    HIGH_MEM_QUEUE: {},
}

# If we're a worker on the high_mem queue, set ourselves to die after processing
# one request to avoid having memory leaks take down the worker server. This env
# var is set in /etc/init/edx-workers.conf -- this should probably be replaced
# with some celery API call to see what queue we started listening to, but I
# don't know what that call is or if it's active at this point in the code.
if os.environ.get('QUEUE') == 'high_mem':
    CELERYD_MAX_TASKS_PER_CHILD = 1

CELERYBEAT_SCHEDULE = {}  # For scheduling tasks, entries can be added to this dict

ALLOWED_HOSTS = [
    "*",
    LMS_BASE,
    PREVIEW_LMS_BASE,
]

# Enable automatic transaction management on all databases
# https://docs.djangoproject.com/en/1.8/topics/db/transactions/#tying-transactions-to-http-requests
# This needs to be true for all databases
for database_name in DATABASES:
    DATABASES[database_name]['ATOMIC_REQUESTS'] = True

MONGODB_LOG = {}

##### Individual Due Date Extensions #####
if FEATURES.get('INDIVIDUAL_DUE_DATES'):
    FIELD_OVERRIDE_PROVIDERS += (
        'courseware.student_field_overrides.IndividualStudentOverrideProvider',
    )

##### Self-Paced Course Due Dates #####
FIELD_OVERRIDE_PROVIDERS += (
    'courseware.self_paced_overrides.SelfPacedDateOverrideProvider',
)



###################################################################################################

from xmodule.modulestore.modulestore_settings import update_module_store_settings

update_module_store_settings(
    MODULESTORE,
    doc_store_settings=DOC_STORE_CONFIG,
    module_store_options={'fs_root': DATA_DIR},
    xml_store_options={'data_dir': DATA_DIR},)

# We move split mongo store at the top of store lists to make it the
# default one. Note that the 'modulestore' app makes split mongo
# available even if you have not define it in your settings.
update_module_store_settings(MODULESTORE, default_store='split')


CACHES['default']['LOCATION'] = ['memcached:11211']
CACHES['general']['LOCATION'] = ['memcached:11211']
CACHES['celery']['LOCATION'] = ['memcached:11211']
CACHES['staticfiles']['LOCATION'] = ['memcached:11211']
CACHES['mongo_metadata_inheritance']['LOCATION'] = ['memcached:11211']


LOG_DIR = '/edx/var/logs/edx'

ENVIRONMENT = 'dogwood-fun'

FEATURES['ENABLE_DISCUSSION_SERVICE'] = False

ALLOWED_HOSTS = ["*"]

LOGGING['handlers'].update(
    local={'class': 'logging.NullHandler'},
    tracking={'class': 'logging.NullHandler'},
)

# Profile image upload
PROFILE_IMAGE_BACKEND = {
    'class': 'storages.backends.overwrite.OverwriteStorage',
    'options': {
        'location': os.path.join(MEDIA_ROOT, 'profile-images/'),
        'base_url': os.path.join(MEDIA_URL, 'profile-images/'),
    },
}





STATIC_ROOT = os.environ.get('STATIC_ROOT', '/edx/var/edxapp/staticfiles/lms')
STATIC_URL = os.environ.get('STATIC_URL', '/static/')

INSTALLED_APPS += (
    'rest_framework.authtoken',

    'backoffice',
    'fun',
    'funsite',
    'fun_api',
    'fun_certificates',
    'fun_instructor',
    'contact',
    'course_dashboard',
    'courses',
    'courses_api',
    'course_pages',
    'newsfeed',
    'universities',
    'videoproviders',

    'haystack',
    'easy_thumbnails',
    'bootstrapform',
    'ckeditor',
    'raven.contrib.django.raven_compat',
    'pure_pagination',

    'payment',
    'payment_api',

    'forum_contributors',
    'selftest',
    # this is an xblock we add to applications to allow syncdb of its models
    'password_container',
    'teachers',
    'faq',
    'edx_gea',
)
INSTALLED_APPS += get_proctoru_app_if_available()

ROOT_URLCONF = 'fun.lms.urls'

update_logging_config(LOGGING)

# Disable S3 file storage
del DEFAULT_FILE_STORAGE

# those values also have to be in env.json file,
# because pavlib.utils.envs reads it to build asset's preprocessing commands
FEATURES['ENABLE_MKTG_SITE'] = False

SITE_NAME = LMS_BASE


MIDDLEWARE_CLASSES += LEGAL_ACCEPTANCE_MIDDLEWARE

# MKTG_URL_LINK_MAP links are named url reverses belonging to Django project
# (also see MKTG_URLS in cms.py)
MKTG_URL_LINK_MAP = {
    "ABOUT": "about",
    "HONOR": "honor",
    "HOW-IT-WORKS": "how-it-works",
    "TOS": "tos",
    "FAQ": None,
    "PRIVACY": "privacy",
    "CONTACT": None,
    "UNSUPPORTED-BROWSER": "unsupported-browser",
    "LICENSES": "licenses",
    "LEGAL": "legal",
    "COPYRIGHTS": None,
    "ROOT": 'root',
    'COURSES': 'fun-courses:index',
}
FUN_MKTG_URLS = {}

# hide spocs from course list
FEATURES['ACCESS_REQUIRE_STAFF_FOR_COURSE'] = True
FEATURES['ALLOW_COURSE_STAFF_GRADE_DOWNLOADS'] = True
FEATURES['AUTH_USE_OPENID_PROVIDER'] = True
FEATURES['ADVANCED_SECURITY'] = False
FEATURES['AUTOMATIC_AUTH_FOR_TESTING'] = False
FEATURES['CERTIFICATES_ENABLED'] = True
FEATURES['CERTIFICATES_HTML_VIEW'] = True
FEATURES['ENABLE_COURSEWARE_INDEX'] = False
FEATURES['ENABLE_DISCUSSION_SERVICE'] = True
FEATURES['ENABLE_DJANGO_ADMIN_SITE'] = True
FEATURES['ENABLE_INSTRUCTOR_ANALYTICS'] = False
FEATURES['ENABLE_MAX_FAILED_LOGIN_ATTEMPTS'] = False
FEATURES['ENABLE_S3_GRADE_DOWNLOADS'] = True
FEATURES['PREVIEW_LMS_BASE'] = PREVIEW_LMS_BASE
FEATURES['SUBDOMAIN_BRANDING'] = False
FEATURES['SUBDOMAIN_COURSE_LISTINGS'] = False
FEATURES['ENFORCE_PASSWORD_POLICY'] = True
FEATURES['ENABLE_CONTENT_LIBRARIES'] = True

TEMPLATES[0]['OPTIONS']['context_processors'] += (
    'fun.context_processor.fun_settings',)

# Add FUN applications templates directories to MAKO template finder before edX's ones
MAKO_TEMPLATES['main'] = [
    # overrides template in edx-platform/lms/templates
    FUN_BASE_ROOT / 'funsite/templates/lms',
    FUN_BASE_ROOT / 'funsite/templates',
    FUN_BASE_ROOT / 'course_pages/templates',
    FUN_BASE_ROOT / 'payment/templates',
    FUN_BASE_ROOT / 'course_dashboard/templates',
    FUN_BASE_ROOT / 'newsfeed/templates',
    FUN_BASE_ROOT / 'fun_certificates/templates',
] + MAKO_TEMPLATES['main']

# Add funsite templates directory to Django templates finder.
TEMPLATES[0]['DIRS'].insert(0, FUN_BASE_ROOT / 'funsite/templates/lms')

# Enable legal page
MKTG_URL_LINK_MAP['LEGAL'] = 'legal'

# Allow sending bulk e-mails for all courses
FEATURES['REQUIRE_COURSE_EMAIL_AUTH'] = False

# Access to sysadmin view (users, courses information. User has to be staff, see navigation.html)
FEATURES['ENABLE_SYSADMIN_DASHBOARD'] = False

# Registration form fields ('required', 'optional', 'hidden')
REGISTRATION_EXTRA_FIELDS = {
    'level_of_education': 'optional',
    'gender': 'optional',
    'year_of_birth': 'optional',
    'mailing_address': 'optional',
    'goals': 'optional',
    'honor_code': 'required',
    'city': 'required',
    'country': 'required',
}

SITE_VARIANT = 'lms'

FUN_SMALL_LOGO_RELATIVE_PATH = 'funsite/images/logos/funmooc173.png'
FUN_BIG_LOGO_RELATIVE_PATH = 'funsite/images/logos/funmoocfp.png'

# Certificates related settings
CERTIFICATE_BASE_URL = '/attestations/'
CERTIFICATES_DIRECTORY = '/edx/var/edxapp/attestations/'
FUN_LOGO_PATH = FUN_BASE_ROOT / 'funsite/static' / FUN_BIG_LOGO_RELATIVE_PATH
FUN_ATTESTATION_LOGO_PATH = FUN_BASE_ROOT / \
    'funsite/static' / 'funsite/images/logos/funmoocattest.png'
STUDENT_NAME_FOR_TEST_CERTIFICATE = 'Test User'

# Grades related settings
GRADES_DOWNLOAD = {
    'STORAGE_TYPE': 'localfs',
    'BUCKET': 'edx-grades',
    'ROOT_PATH': '/edx/var/edxapp/grades',
}
GRADES_DOWNLOAD_ROUTING_KEY = None


# Our new home page is so shiny and chrome that users must see it more often
FEATURES['ALWAYS_REDIRECT_HOMEPAGE_TO_DASHBOARD_FOR_AUTHENTICATED_USER'] = False

# used by pure-pagination app, https://github.com/jamespacileo/django-pure-pagination
# for information about the constants :
# https://camo.githubusercontent.com/51defa6771f5db2826a1869eca7bed82d9fb3120/687474703a2f2f692e696d6775722e636f6d2f4c437172742e676966
PAGINATION_SETTINGS = {
    # same formatting as in github issues, seems to be sane.
    'PAGE_RANGE_DISPLAYED': 4,
    'MARGIN_PAGES_DISPLAYED': 2,
}

NUMBER_DAYS_TOO_LATE = 31

# Default visibility of student's profile to other students
ACCOUNT_VISIBILITY_CONFIGURATION["default_visibility"] = "private"

# easy-thumbnails
#SOUTH_MIGRATION_MODULES['easy_thumbnails'] = 'easy_thumbnails.south_migrations'


# Add our v3 CSS and JS files to assets compilation pipeline to make them available in courseware.
# On FUN v3 frontend, which do not use edX's templates, those files are loaded
# by funsite/templates/funsite/parts/base.html and css/lms-main.css

PIPELINE_CSS['style-vendor']['source_filenames'].append(
    'fun/css/cookie-banner.css')
PIPELINE_CSS['style-vendor']['source_filenames'].append(
    'funsite/css/header.css')
PIPELINE_CSS['style-vendor']['source_filenames'].append(
    'funsite/css/footer.css')

#  can't find any common group
for group in ['base_vendor', 'main_vendor']:
    PIPELINE_JS[group]['source_filenames'].append('funsite/js/header.js')
    PIPELINE_JS[group]['source_filenames'].append('fun/js/cookie-banner.js')

# display a search box in student's dashboard to search in courses he is enrolled in.
FEATURES['ENABLE_DASHBOARD_SEARCH'] = True
# display a search box and enable Backbone app on edX's course liste page which we do not use.
FEATURES['ENABLE_COURSE_DISCOVERY'] = False

# Payment
FEATURES["ENABLE_OAUTH2_PROVIDER"] = True
FEATURES['ENABLE_PAYMENT_FAKE'] = True
FEATURES["ENABLE_CREDIT_API"] = True
FEATURES["ENABLE_CREDIT_ELIGIBILITY"] = True
FEATURES["ENABLE_MOBILE_REST_API"] = True
FEATURES['ENABLE_COMBINED_LOGIN_REGISTRATION'] = False

PAID_COURSE_REGISTRATION_CURRENCY = ["EUR", "€"]

EDX_API_KEY = 'test'

ECOMMERCE_API_SIGNING_KEY = 'test'
ECOMMERCE_API_URL = "http://localhost:8080/api/v2/"
ECOMMERCE_PUBLIC_URL_ROOT = "http://localhost:8080/"
ECOMMERCE_NOTIFICATION_URL = 'http://localhost:8080/payment/paybox/notify/'
ECOMMERCE_SERVICE_WORKER_USERNAME = 'ecommerce_worker'

JWT_ISSUER = "http://localhost:8000/oauth2"
JWT_EXPIRATION = 30

OAUTH_ENFORCE_SECURE = False
OAUTH_OIDC_ISSUER = "http://localhost:8000/oauth2"

# Append fun header script to verification pages
# DOGWOOD: probablement plus nécessaire
# PIPELINE_JS['rwd_header']['source_filenames'].append('funsite/js/header.js')

# A user is verified if he has an approved SoftwareSecurePhotoVerification entry
# this setting will create a dummy SoftwareSecurePhotoVerification for user in paybox success callback view
# I think it's better to create a dummy one than to remove verifying process in edX
FUN_ECOMMERCE_DEBUG_NO_NOTIFICATION = False

# when True this setting add a link in instructor dashbord to analytics insigt service
ANALYTICS_DASHBOARD_URL = False


PROCTORU_URL_TEST = "https://test-it-out.proctoru.com"

