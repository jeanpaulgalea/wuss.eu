from django.conf.urls import patterns, url

from .views import shorten, redirect, qr, modify


hash = '(?P<hash>[a-zA-Z0-9]{3,9})'
uuid = '(?P<uuid>[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12})'

urlpatterns = patterns('',
    url(r'^$',                    view=shorten, name='homepage'),
    url(r'^'+hash+'/?$',          view=redirect, name='redirect'),
    url(r'^'+hash+'/qr/?$',       view=qr, name='display-qr-image'),
    url(r'^'+hash+'/qr/save/?$',  qr, {'save': True}, name='download-qr-image'),
    url(r'^'+hash+'/'+uuid+'/?$', view=modify, name='edit-link'),
)
