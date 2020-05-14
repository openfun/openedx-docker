"""Django static file storage backend for OpenEdX."""
from django.conf import settings

from openedx.core.storage import ProductionStorage


class CDNProductionStorage(ProductionStorage):
    """Open edX production static files storage backend that can be placed behing a CDN."""

    def url(self, name, force=False):
        """Prepend static files path by the CDN base url when configured in settings."""
        url = super(CDNProductionStorage, self).url(name, force=force)

        cdn_base_url = getattr(settings, "CDN_BASE_URL", None)
        if cdn_base_url:
            url = "{:s}{:s}".format(cdn_base_url, url)

        return url
