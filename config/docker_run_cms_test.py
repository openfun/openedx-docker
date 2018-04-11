# -*- coding: utf-8 -*-

from .shared_test import *

ENVIRONMENT = 'test'

# set working directory to fun-apps to run only our tests
os.chdir(FUN_BASE_ROOT)

############# Disable useless logging
import logging
logging.getLogger("edxmako.shortcuts").setLevel(logging.ERROR)

############ If you modify settings below this line don't forget to modify them both in lms/test.py and cms/test.py
from path import path

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
NOSE_ARGS = nose_args(REPO_ROOT, 'cms')

TEST_ROOT = path("test_root")
COMMON_TEST_DATA_ROOT = COMMON_ROOT / "test" / "data"
DATABASES = databases(TEST_ROOT)

################# mongodb
MONGO_PORT_NUM = int(os.environ.get('EDXAPP_TEST_MONGO_PORT', '27017'))
MONGO_HOST = os.environ.get('EDXAPP_TEST_MONGO_HOST', 'mongodb')
CONTENTSTORE = contentstore(MONGO_HOST, MONGO_PORT_NUM)

PASSWORD_HASHERS = password_hashers
STATICFILES_STORAGE = 'pipeline.storage.NonPackagingPipelineStorage'
PIPELINE_ENABLED = False

CACHES.update(caches)

################ Disable Django debug toolbar
INSTALLED_APPS = tuple(
    [app for app in INSTALLED_APPS if app not in DEBUG_TOOLBAR_INSTALLED_APPS])
MIDDLEWARE_CLASSES = tuple(
    [m for m in MIDDLEWARE_CLASSES if m not in DEBUG_TOOLBAR_MIDDLEWARE_CLASSES])

# Disable costly calls to publish signals
COURSE_SIGNALS_DISABLED = True

# From Django 1.7 `syndb` do not exists anymore then `migrate` is used to create db
# it makes test database creation very long.
# See: https://groups.google.com/d/msg/django-developers/PWPj3etj3-U/QTpjBvD2QMcJ
MIGRATION_MODULES = dict((app, '%s.fake_migrations' % app)
                         for app in INSTALLED_APPS)
