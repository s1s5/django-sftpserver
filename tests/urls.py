# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.conf.urls import url, include

from django_sftpserver.urls import urlpatterns as django_sftpserver_urls

urlpatterns = [
    url(r'^', include((django_sftpserver_urls, 'django_sftpserver'), namespace='django_sftpserver')),
]
