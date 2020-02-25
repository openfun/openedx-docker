from docker_run_development import *


ENVIRONMENT = 'test'

TEST_ROOT = "/data/test_root"
COMMON_TEST_DATA_ROOT = COMMON_ROOT / "test" / "data"
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': TEST_ROOT + '/db/fun.db'
    },
}

os.environ["EDXAPP_TEST_MONGO_HOST"] = "mongodb"
os.environ["EDXAPP_TEST_MONGO_PORT"] = "27017"

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

SECRET_KEY = "foo"

PIPELINE_ENABLED = False

STATICFILES_STORAGE = 'openedx.core.storage.DevelopmentStorage'

FEATURES['ENABLE_DISCUSSION_SERVICE'] = False

ALLOWED_HOSTS = ["*"]

LOGGING['handlers'].update(
    local={'class': 'logging.NullHandler'},
    tracking={'class': 'logging.NullHandler'},
)