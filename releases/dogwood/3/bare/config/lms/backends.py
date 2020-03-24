# -*- coding: utf-8 -*-

from ratelimitbackend.backends import RateLimitModelBackend


class ProxyRateLimitModelBackend(RateLimitModelBackend):
    """A rate limiting Backend that works behind a proxy."""

    def get_ip(self, request):
        """Return the end user address string as set by proxies."""
        return request.META["HTTP_X_FORWARDED_FOR"]
