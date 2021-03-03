"""
OEE urls
We define this file as root url (ROOT_URLCONF) to override and extend
edx-platform's CMS routes
"""
from __future__ import absolute_import, unicode_literals

from django.conf.urls import include, url

from cms.urls import urlpatterns  # pylint: disable=import-error


urlpatterns += [
    url(r'^openassessment/fileupload/', include('openassessment.fileupload.urls')),
]
