"""
Django file storage backend for the LMS that works behind a CDN.
"""
from django.contrib.staticfiles.storage import ManifestStaticFilesStorage

from pipeline.storage import PipelineMixin
from require.storage import OptimizedFilesMixin


class LMSManifestStaticFilesStorage(
    OptimizedFilesMixin, PipelineMixin, ManifestStaticFilesStorage
):
    """
    This static files storage backend works when static files are in the `edxapp-nginx` image.
    OptimizedFilesMixin: https://github.com/etianen/django-require
    PipelineMixin: https://github.com/jazzband/django-pipeline
    """

