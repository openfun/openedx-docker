from docker_run_production import *
from .utils import Configuration

from path import path
from .. import test
import logging

# test settings common to lms and cms
import os
import tempfile

############# Disable useless logging
logging.getLogger("audit").setLevel(logging.WARN)
logging.getLogger("django_comment_client.utils").setLevel(logging.WARN)
logging.getLogger('edx.celery.task').setLevel(logging.ERROR)
logging.getLogger("factory").setLevel(logging.WARN)
logging.getLogger("googleapiclient.discovery").setLevel(logging.ERROR)
logging.getLogger('instructor_task.api_helper').setLevel(logging.ERROR)
logging.getLogger('instructor_task.tasks_helper').setLevel(logging.ERROR)
logging.getLogger(
    "raven.contrib.django.client.DjangoClient").setLevel(logging.WARN)
logging.getLogger('util.models').setLevel(logging.CRITICAL)
logging.getLogger('xmodule.modulestore.django').setLevel(logging.ERROR)


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
mongo_host = os.environ.get('EDXAPP_TEST_MONGO_HOST', 'localhost')


def contentstore(host, port):
    return {
        'ENGINE': 'xmodule.contentstore.mongo.MongoContentStore',
        'DOC_STORE_CONFIG': {
            'ssl': False,
            'user': None,
            'password': '',
            'replicaSet': None,
            'read_preference': 'PRIMARY',
            'host': 'mongodb',
            'db': 'testdb',
            'port': 27017,
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

# Disable access to videofront in tests
VIDEOFRONT_URL = 'http://video'





ENVIRONMENT = 'test'

############# Disable useless logging
logging.getLogger("edxmako.shortcuts").setLevel(logging.ERROR)

############ If you modify settings below this line don't forget to modify them both in lms/test.py and cms/test.py

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
NOSE_ARGS = nose_args(REPO_ROOT, 'lms')

TEST_ROOT = path("test_root")
COMMON_TEST_DATA_ROOT = COMMON_ROOT / "test" / "data"
DATABASES = databases(TEST_ROOT)

################# mongodb

MONGO_PORT_NUM = int(os.environ.get('EDXAPP_TEST_MONGO_PORT', '27017'))
MONGO_HOST = os.environ.get('EDXAPP_TEST_MONGO_HOST', 'mongodb')
CONTENTSTORE = contentstore(MONGO_HOST, MONGO_PORT_NUM)

PASSWORD_HASHERS =password_hashers
STATICFILES_STORAGE = 'pipeline.storage.NonPackagingPipelineStorage'
PIPELINE_ENABLED = False

CACHES.update(caches)

################ Disable Django debug toolbar
#INSTALLED_APPS = tuple(
#    [app for app in INSTALLED_APPS if app not in DEBUG_TOOLBAR_INSTALLED_APPS])
#MIDDLEWARE_CLASSES = tuple(
#    [m for m in MIDDLEWARE_CLASSES if m not in DEBUG_TOOLBAR_MIDDLEWARE_CLASSES])

# Disable costly calls to publish signals
COURSE_SIGNALS_DISABLED = True

# From Django 1.7 `syndb` do not exists anymore then `migrate` is used to create db
# it makes test database creation very long.
# See: https://groups.google.com/d/msg/django-developers/PWPj3etj3-U/QTpjBvD2QMcJ
MIGRATION_MODULES = dict((app, '%s.fake_migrations' % app)
                         for app in INSTALLED_APPS)

# Remove LEGAL_ACCEPTANCE_MIDDLEWARE
#MIDDLEWARE_CLASSES = [
#    mw for mw in MIDDLEWARE_CLASSES if mw != LEGAL_ACCEPTANCE_MIDDLEWARE[0]]
