from django.conf.urls import patterns, include, url
from django_ui import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'django_ui.views.home', name='home'),
    # url(r'^django_ui/', include('django_ui.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^ui/', include('f4k_ui.urls')),
    url(r'^accounts/', include('registration.backends.simple.urls')),
    
    #redirect after registering
    (r'^users/.+?/$', 'f4k_ui.views.afterlogin'),
)

#..rest of url.py config...
urlpatterns += staticfiles_urlpatterns()

if settings.DEBUG:
	urlpatterns += patterns ('',
		url(r'^django_ui_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
		url(r'^django_ui_static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
	)	

