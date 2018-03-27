from .dev import *
from path import path

ENVIRONMENT = 'test'

# set working directory to fun-apps to run only our tests
os.chdir(FUN_BASE_ROOT)

############# Disable useless logging
import logging
logging.getLogger("backoffice.views").setLevel(logging.ERROR)
logging.getLogger("edxmako.shortcuts").setLevel(logging.ERROR)

################ Microsite test settings

FAKE_MICROSITE = {
    "domain_prefix": "testmicrosite",
    "university": "test_microsite",
    "platform_name": "Test Microsite",
    "logo_image_url": "test_microsite/images/header-logo.png",
    "email_from_address": "test_microsite@edx.org",
    "payment_support_email": "test_microsite@edx.org",
    "ENABLE_MKTG_SITE": False,
    "SITE_NAME": "test_microsite.localhost",
    "course_org_filter": "TestMicrositeX",
    "course_about_show_social_links": False,
    "css_overrides_file": "test_microsite/css/test_microsite.css",
    "show_partners": False,
    "show_homepage_promo_video": False,
    "course_index_overlay_text": "This is a Test Microsite Overlay Text.",
    "course_index_overlay_logo_file": "test_microsite/images/header-logo.png",
    "homepage_overlay_html": "<h1>This is a Test Microsite Overlay HTML</h1>",
    "ALWAYS_REDIRECT_HOMEPAGE_TO_DASHBOARD_FOR_AUTHENTICATED_USER": False,
    "COURSE_CATALOG_VISIBILITY_PERMISSION": "see_in_catalog",
    "COURSE_ABOUT_VISIBILITY_PERMISSION": "see_about_page",
    "ENABLE_SHOPPING_CART": True,
    "ENABLE_PAID_COURSE_REGISTRATION": True,
    "SESSION_COOKIE_DOMAIN": "test_microsite.localhost",
}

MICROSITE_ROOT_DIR = path("/edx/app/edxapp/fun-microsites")
MICROSITE_TEST_HOSTNAME = 'testmicrosite.testserver'

############ If you modify settings below this line don't forget to modify them both in lms/test.py and cms/test.py
import common_test as test


TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
NOSE_ARGS = test.nose_args(REPO_ROOT, 'lms')

TEST_ROOT = path("test_root")
COMMON_TEST_DATA_ROOT = COMMON_ROOT / "test" / "data"
DATABASES = test.databases(TEST_ROOT)

################# mongodb
MONGO_PORT_NUM = int(os.environ.get('EDXAPP_TEST_MONGO_PORT', '27017'))
MONGO_HOST = os.environ.get('EDXAPP_TEST_MONGO_HOST', 'mongodb')
CONTENTSTORE = test.contentstore(MONGO_HOST, MONGO_PORT_NUM)

PASSWORD_HASHERS = test.password_hashers
STATICFILES_STORAGE = 'pipeline.storage.NonPackagingPipelineStorage'
PIPELINE_ENABLED = False

CACHES.update(test.caches)

################ Disable Django debug toolbar
INSTALLED_APPS = tuple(
    [app for app in INSTALLED_APPS if app not in DEBUG_TOOLBAR_INSTALLED_APPS])
MIDDLEWARE_CLASSES = tuple(
    [m for m in MIDDLEWARE_CLASSES if m not in DEBUG_TOOLBAR_MIDDLEWARE_CLASSES])

FEATURES['USE_MICROSITES'] = False

# Disable costly calls to publish signals
COURSE_SIGNALS_DISABLED = True

# From Django 1.7 `syndb` do not exists anymore then `migrate` is used to create db
# it makes test database creation very long.
# See: https://groups.google.com/d/msg/django-developers/PWPj3etj3-U/QTpjBvD2QMcJ
MIGRATION_MODULES = dict((app, '%s.fake_migrations' % app)
                         for app in INSTALLED_APPS)
