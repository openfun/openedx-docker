# -*- coding: utf-8 -*-


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

import os, sys
from path import path

BASE_ROOT = path('/edx/app/edxapp/')
BASE_DATA = path('/edx/var/edxapp/')

FUN_BASE_ROOT = BASE_ROOT / 'fun-apps'
sys.path.append(FUN_BASE_ROOT)

os.environ['BASE_ROOT'] = BASE_ROOT
os.environ['CONFIG_ROOT'] = BASE_ROOT
os.environ['SERVICE_VARIANT'] = 'cms'
os.environ['SHARED_ROOT'] = BASE_DATA / 'shared'

os.environ['STATIC_ROOT_BASE'] = '/edx/var/edxapp/static'
os.environ['STATIC_ROOT'] = '/edx/var/edxapp/static/cms'
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

from fun.envs.cms.common import *

from .docker_run_common import *  # pylint: disable=wildcard-import, unused-wildcard-import

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

STATIC_ROOT = '/edx/var/edxapp/static/cms'
STATIC_ROOT_BASE = '/edx/var/edxapp/static'
STATIC_URL = '/static/'

MEDIA_ROOT = '/edx/var/edxapp/media'
MEDIA_URL = '/media/'

LOG_DIR = '/edx/var/logs/edx'

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
