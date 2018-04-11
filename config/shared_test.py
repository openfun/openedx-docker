# test settings common to lms and cms
import os
import tempfile

from .docker_run_lms_dev import *


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'console': {
            'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'console',
        },
    },
    'loggers': {
        '': {
            'level': 'WARNING',
            'handlers': ['console'],
        },
    },
}



# Special mongodb configuration when unittest inherit from ModuleStoreTestCase
# See common/lib/xmodule/xmodule/modulestore/tests/mongo_connection.py
os.environ['EDXAPP_TEST_MONGO_PORT'] = '27017'
os.environ['EDXAPP_TEST_MONGO_HOST'] = 'mongodb'

def nose_args(repo_root, service):
    return [
        '--id-file', repo_root / '.testids' / service / 'noseids',
        '--xunit-file', repo_root / 'reports' / service / 'nosetests.xml',
        '--nologcapture',
    ]


def databases(test_root):
    return {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': test_root / 'db' / 'fun.db'
        },
    }


mongo_port_num = int(os.environ.get('EDXAPP_TEST_MONGO_PORT', '27017'))
mongo_host = os.environ.get('EDXAPP_TEST_MONGO_HOST', 'mongodb')


def contentstore(host, port):
    return {
        'ENGINE': 'xmodule.contentstore.mongo.MongoContentStore',
        'DOC_STORE_CONFIG': {
            'host': host,
            'db': 'xcontent',
            'port': port,
        }
    }


password_hashers = (
    'django.contrib.auth.hashers.SHA1PasswordHasher',
    'django.contrib.auth.hashers.MD5PasswordHasher',
)

caches = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'edx_loc_mem_cache',
        'KEY_FUNCTION': 'util.memcache.safe_key',
    },

    'general': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        'KEY_PREFIX': 'general',
        'VERSION': 4,
        'KEY_FUNCTION': 'util.memcache.safe_key',
    },

    'mongo_metadata_inheritance': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': os.path.join(tempfile.gettempdir(), 'mongo_metadata_inheritance'),
        'TIMEOUT': 300,
        'KEY_FUNCTION': 'util.memcache.safe_key',
    },
    'loc_cache': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'edx_location_mem_cache',
    },

}