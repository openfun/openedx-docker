# -*- coding: utf-8 -*-

from cms.envs.common import *

from lms.envs.fun.lms_cms_common import *


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

DATA_DIR = '/data/data'

# This constant as nothing to do with github.
# Path is used to store tar.gz courses before import process
GITHUB_REPO_ROOT = DATA_DIR

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
