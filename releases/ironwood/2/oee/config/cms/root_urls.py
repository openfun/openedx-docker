"""
OEE urls
We define this file as root url (ROOT_URLCONF) to override and extend
edx-platform's CMS routes
"""
from __future__ import absolute_import, unicode_literals

from cms.urls import urlpatterns  # pylint: disable=import-error
from openassessment.fileupload.urls import urlpatterns as ora_urlpatterns


urlpatterns += ora_urlpatterns
