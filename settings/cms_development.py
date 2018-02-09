from .devstack import *

update_module_store_settings(MODULESTORE, doc_store_settings=DOC_STORE_CONFIG)

STATIC_ROOT = '/data/static/cms'
STATIC_URL = '/static/'
MEDIA_ROOT = '/data/media'
LOG_DIR = '/data/log'

FEATURES['ENABLE_DISCUSSION_SERVICE'] = False

ALLOWED_HOSTS = ["*"]

LOGGING['handlers'].update(
    local={'class': 'logging.NullHandler'},
    tracking={'class': 'logging.NullHandler'},
)
