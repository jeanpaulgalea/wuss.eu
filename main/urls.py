from django.conf.urls import patterns, url

from .views import shorten, redirect, modify

hash = '([a-zA-Z0-9]{3,9})'
uuid = '([a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12})'

urlpatterns = patterns('',
    url(r'^$',                    view=shorten),
    url(r'^'+hash+'/?$',          view=redirect),
    url(r'^'+hash+'/'+uuid+'/?$', view=modify),
)