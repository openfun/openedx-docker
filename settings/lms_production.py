from .aws import *

update_module_store_settings(MODULESTORE, doc_store_settings=DOC_STORE_CONFIG)

STATIC_ROOT = '/data/static/lms'
MEDIA_ROOT = '/data/media'
LOG_DIR = '/data/log'

LOGGING['handlers'].update(
    local={'class': 'logging.NullHandler'},
    tracking={'class': 'logging.NullHandler'},
)
