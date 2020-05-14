"""Django static file storage backend for OpenEdX."""
from django.conf import settings

from pipeline.storage import PipelineCachedStorage

from openedx.core.storage import ProductionStorage


class CDNMixin(object):
    """Mixin to activate CDN urls on a static files storage backend."""

    def url(self, name, force=False):
        """Prepend static files path by the CDN base url when configured in settings."""
        url = super(CDNMixin, self).url(name, force=force)

        cdn_base_url = getattr(settings, "CDN_BASE_URL", None)
        if cdn_base_url:
            url = "{:s}{:s}".format(cdn_base_url, url)

        return url


class CDNProductionStorage(CDNMixin, ProductionStorage):
    """Open edX LMS production static files storage backend that can be placed behing a CDN."""


class CDNPipelineCachedStorage(CDNMixin, PipelineCachedStorage):
    """Open edX Studio production static files storage backend that can be placed behing a CDN."""
