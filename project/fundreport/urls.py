from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('fundreport.views',
    # This URL serves the index page:
    url(r'^$', 'index',),

    # This URL accepts a fund ID and generates
    # the corresponding PDF
    url(r'^fundreport/(?P<id>\d+).pdf$', 'fundreport',),
)
