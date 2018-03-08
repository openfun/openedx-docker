from .devstack import *

DATA_DIR = '/data/data'
GITHUB_REPO_ROOT = DATA_DIR  # weirdly used for path to upload course to import

update_module_store_settings(
        MODULESTORE,
        doc_store_settings=DOC_STORE_CONFIG,
        module_store_options={'fs_root': DATA_DIR},
        xml_store_options={'data_dir': DATA_DIR},)

STATIC_ROOT = '/edx/var/edxapp/static/cms'
STATIC_URL = '/static/'
MEDIA_ROOT = '/edx/var/edxapp/media'
LOG_DIR = '/edx/var/logs/edx'


FEATURES['ENABLE_DISCUSSION_SERVICE'] = False

ALLOWED_HOSTS = ["*"]

LOGGING['handlers'].update(
    local={'class': 'logging.NullHandler'},
    tracking={'class': 'logging.NullHandler'},
)

