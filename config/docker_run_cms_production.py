# -*- coding: utf-8 -*-

from datetime import timedelta

from celery.schedules import crontab

from cms.envs.common import *

from lms.envs.fun.shared_settings import *


############# from cms.auth.json ############

CONTENTSTORE = {
    'ENGINE': 'xmodule.contentstore.mongo.MongoContentStore',
    'DOC_STORE_CONFIG': {
        'db': 'edxapp',
        'host': 'mongodb'
    }
}

DOC_STORE_CONFIG = {
    'db': 'edxapp',
    'host': 'mongodb'
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'edxapp',
        'USER': 'fun',
        'PASSWORD': 'password',
        'HOST': 'mysql',
        'PORT': '3306',
        'ATOMIC_REQUESTS': True
    }
}

###############################

import os
import sys
from path import path

BASE_ROOT = path('/edx/app/edxapp/')
BASE_DATA = path('/edx/var/edxapp/')

FUN_BASE_ROOT = BASE_ROOT / 'fun-apps'
sys.path.append(FUN_BASE_ROOT)

CONFIG_ROOT = BASE_ROOT
SERVICE_VARIANT = 'cms'
SHARED_ROOT = BASE_DATA / 'shared'

STATIC_ROOT_BASE = '/edx/var/edxapp/static'
STATIC_ROOT = '/edx/var/edxapp/static/cms'
STATIC_URL = '/static/'

MEDIA_ROOT = '/edx/var/edxapp/media'
MEDIA_URL = '/media/'

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'courses.search_indexes.ConfigurableElasticSearchEngine',
        'URL': 'http://localhost:9200/',
        'INDEX_NAME': 'haystack',
    },
}


BROKER_URL = 'amqp://guest@rabbitmq:5672'
MEMCACHED_URL = 'memcached:11211'

update_module_store_settings(
    MODULESTORE,
    doc_store_settings=DOC_STORE_CONFIG,
    module_store_options={'fs_root': DATA_DIR},
    xml_store_options={'data_dir': DATA_DIR},)

CACHES['default']['LOCATION'] = ['memcached:11211']
CACHES['general']['LOCATION'] = ['memcached:11211']
CACHES['celery']['LOCATION'] = ['memcached:11211']
CACHES['staticfiles']['LOCATION'] = ['memcached:11211']
CACHES['mongo_metadata_inheritance']['LOCATION'] = ['memcached:11211']

CMS_SEGMENT_KEY = None

LOG_DIR = '/edx/var/logs/edx'

FEATURES['ENABLE_DISCUSSION_SERVICE'] = False

ALLOWED_HOSTS = ["*"]

from openedx.core.lib.logsettings import get_logger_config

LOGGING = get_logger_config(LOG_DIR,
                            logging_env='sandbox',
                            debug=False,
                            service_variant=SERVICE_VARIANT)




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


######################################################################


INSTALLED_APPS += (
    'fun',
    'videoproviders',
    'teachers',
    'courses',
    'haystack',
    'universities',

    'easy_thumbnails',
    'ckeditor',
    'selftest',
    'password_container',
    'raven.contrib.django.raven_compat',
    'edx_gea'
)
INSTALLED_APPS += get_proctoru_app_if_available()

ROOT_URLCONF = 'fun.cms.urls'

update_logging_config(LOGGING)

# add 'theme/cms/templates' directory to MAKO template finder to override some CMS templates...
MAKO_TEMPLATES['main'].insert(0, ENV_ROOT / 'fun-apps/fun/templates/cms')

# #652 we need this to False for course HTML description to be editable
# but it's for now incompatible with working footpage links
# see cms/djangoapps/contentstore/views/course.py:617
FEATURES['ENABLE_MKTG_SITE'] = False
# MKTG_URLS are absolute urls used when ENABLE_MKTG_SITE is set to True
# As FUN theme is not used in CMS, we can not reverse its static pages like /tos or /privacy
MKTG_URL_LINK_MAP = {}
MKTG_URLS = {}
MKTG_URLS['ROOT'] = 'http://' + LMS_BASE
MKTG_URLS['TOS'] = '/tos'
MKTG_URLS['PRIVACY'] = '/privacy'

MIDDLEWARE_CLASSES += LEGAL_ACCEPTANCE_MIDDLEWARE

# Allow all courses to use advanced components
FEATURES['ALLOW_ALL_ADVANCED_COMPONENTS'] = True
FEATURES['AUTH_USE_OPENID_PROVIDER'] = True
FEATURES['AUTOMATIC_AUTH_FOR_TESTING'] = False
FEATURES['ADVANCED_SECURITY'] = False
FEATURES['CERTIFICATES_ENABLED'] = True
FEATURES['CERTIFICATES_HTML_VIEW'] = True
FEATURES['ENABLE_CONTENT_LIBRARIES'] = True
# restrain user who can create course in studio to granted ones in CourseCreator table
FEATURES['ENABLE_CREATOR_GROUP'] = True
FEATURES['ENABLE_DISCUSSION_SERVICE'] = True
FEATURES['ENABLE_DJANGO_ADMIN_SITE'] = True
FEATURES['ENABLE_INSTRUCTOR_ANALYTICS'] = True
FEATURES['ENABLE_MAX_FAILED_LOGIN_ATTEMPTS'] = False
FEATURES['ENABLE_S3_GRADE_DOWNLOADS'] = True
FEATURES['ENFORCE_PASSWORD_POLICY'] = True
# used to display Edx Studio logo, see edx-platform/cms/templates/widgets/header.html
FEATURES['IS_EDX_DOMAIN'] = True
FEATURES['SUBDOMAIN_BRANDING'] = False
FEATURES['SUBDOMAIN_COURSE_LISTINGS'] = False
FEATURES['USE_CUSTOM_THEME'] = False

# index courseware content in 'courseware_index' and course meta information in
# 'course_info' after every modification in studio
FEATURES['ENABLE_COURSEWARE_INDEX'] = True


# To use the schedule defined here, you need to have
# a celery beat instance running, for instance, using
# Django `manage.py` with: `celery beat -l INFO`.
# Ex: `fun cms.dev celery beat -l INFO`
CELERYBEAT_SCHEDULE = {
    'update-courses-meta-data-periodically': {
        'task': 'courses.tasks.update_courses_meta_data',
        'schedule': timedelta(hours=3),
    },
    'update-search-index-every-day': {
        'task': 'fun.tasks.update_search_index',
        'schedule': crontab(hour=2, minute=30, day_of_week='*'),
    },
}

# We move split mongo store at the top of store lists to make it the
# default one. Note that the 'modulestore' app makes split mongo
# available even if you have not define it in your settings.
update_module_store_settings(MODULESTORE, default_store='split')
