from .devstack import *

update_module_store_settings(
        MODULESTORE,
        doc_store_settings=DOC_STORE_CONFIG,
        module_store_options={'fs_root': '/data/data'},
        xml_store_options={'data_dir': '/data/data'},)

STATIC_ROOT = '/edx/var/edxapp/static/lms'
STATIC_URL = '/static/'
MEDIA_ROOT = '/edx/var/edxapp/media'
LOG_DIR = '/edx/var/logs/edx'

FEATURES['ENABLE_DISCUSSION_SERVICE'] = False

ALLOWED_HOSTS = ["*"]

LOGGING['handlers'].update(
    local={'class': 'logging.NullHandler'},
    tracking={'class': 'logging.NullHandler'},
)
