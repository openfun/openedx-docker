# -*- coding: utf-8 -*-

# FUN_BASE_ROOT should be added to Python PATH before importing this file
import os, sys
from path import path
BASE_ROOT = path('/app/')
BASE_DATA = path('/data/')

FUN_BASE_ROOT = BASE_ROOT / 'fun-apps'
sys.path.append(FUN_BASE_ROOT)

os.environ['BASE_ROOT'] = BASE_ROOT
os.environ['CONFIG_ROOT'] = BASE_ROOT
os.environ['SERVICE_VARIANT'] = 'lms'
os.environ['SHARED_ROOT'] = BASE_DATA / 'shared'
#os.environ['MEDIA_ROOT'] = BASE_DATA / 'media'
#os.environ['STATIC_ROOT'] = BASE_DATA / 'static' / 'lms'


HAYSTACK_CONNECTIONS = {
        'default': {
            'ENGINE': 'courses.search_indexes.ConfigurableElasticSearchEngine',
            'URL': 'http://localhost:9200/',
            'INDEX_NAME': 'haystack',
        },
    }

from fun.envs.lms.common import *

BROKER_URL = 'amqp://guest@rabbitmq:5672'
MEMCACHED_URL = 'memcached:11211'

DATA_DIR = BASE_DATA / 'data'

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

STATIC_ROOT = '/edx/var/edxapp/static/lms'
STATIC_ROOT_BASE = '/edx/var/edxapp/static'
STATIC_URL = '/static/'

MEDIA_ROOT = '/edx/var/edxapp/media'
MEDIA_URL = '/media/'

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



DEBUG = True
