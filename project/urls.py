from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin
admin.autodiscover()




urlpatterns = patterns('',
    
    # Main site
    url(r'^', include('fundreport.urls')),

    #admin
    url(r'^admin/', include(admin.site.urls)),

)
