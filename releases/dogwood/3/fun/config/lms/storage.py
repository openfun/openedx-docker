"""
Django file storage backend for the LMS that works behind a CDN.
"""
from django.conf import settings
from django.contrib.staticfiles.storage import ManifestStaticFilesStorage

from pipeline.storage import PipelineMixin
from require.storage import OptimizedFilesMixin


class LMSManifestStaticFilesStorage(
    OptimizedFilesMixin, PipelineMixin, ManifestStaticFilesStorage
):
    """
    This static files storage backend works when static files are in the `edxapp-nginx` image,
    eventually placed behing a CDN.

    OptimizedFilesMixin: https://github.com/etianen/django-require
    PipelineMixin: https://github.com/jazzband/django-pipeline
    """

    def url(self, name, force=False):
        """Prepend static files path by the CDN base url when configured in settings."""
        url = super(LMSManifestStaticFilesStorage, self).url(name, force=force)

        cdn_base_url = getattr(settings, "CDN_BASE_URL", None)
        if cdn_base_url:
            url = "{:s}{:s}".format(cdn_base_url, url)

        return url

