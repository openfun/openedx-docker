
# -*- coding: utf-8 -*-

from docker_run import *

DEBUG = True

# Prevent use of aggregated assets, which can't be served by runserver
PIPELINE_ENABLED = False

# Remove LEGAL_ACCEPTANCE_MIDDLEWARE
MIDDLEWARE_CLASSES = [mw for mw in MIDDLEWARE_CLASSES if mw != LEGAL_ACCEPTANCE_MIDDLEWARE[0]]

INSTALLED_APPS += ('django_extensions',)

################################ DEBUG TOOLBAR ################################

DEBUG_TOOLBAR_PANELS = [
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
    'debug_toolbar.panels.profiling.ProfilingPanel',
    'debug_toolbar_mongo.panel.MongoDebugPanel',
]

DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
    'JQUERY_URL': '',  # use jquery from every page
    'SHOW_TOOLBAR_CALLBACK': "{}.true".format(__name__)
}
def true(request):
    return True


DEBUG_TOOLBAR_INSTALLED_APPS = ('debug_toolbar', 'debug_toolbar_mongo',)
DEBUG_TOOLBAR_MIDDLEWARE_CLASSES = (
    'django_comment_client.utils.QueryCountDebugMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

INSTALLED_APPS += DEBUG_TOOLBAR_INSTALLED_APPS
MIDDLEWARE_CLASSES += DEBUG_TOOLBAR_MIDDLEWARE_CLASSES

####################

# Newly created accounts are automaticaly set to verified
FEATURES['AUTOMATIC_VERIFY_STUDENT_IDENTITY_FOR_TESTING'] = True

# Enable automatic creation and login of test user at /auto_auth
FEATURES['ENABLE_AUTO_AUTH'] = True
