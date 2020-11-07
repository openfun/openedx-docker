"""
OEE urls
We define this file as root url (ROOT_URLCONF) to override and extend
edx-platform's LMS routes
"""
from __future__ import absolute_import, unicode_literals

from django.conf.urls import include, url

from lms.urls import urlpatterns  # pylint: disable=import-error
from openassessment.fileupload.urls import urlpatterns as ora_urlpatterns


urlpatterns += [
    # Fonzie API urls
    url(r"^api/", include("fonzie.urls", namespace="fonzie")),
]
urlpatterns+= ora_urlpatterns
