from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^start_session/$', 'processing.views.start_session'),
    url(r'^stop_session/$', 'processing.views.stop_session'),
    url(r'^person_detection/$', 'processing.views.person_detection'),
    url(r'^trigger_processing/$', 'processing.views.trigger_processing'),
    # Examples:
    # url(r'^$', 'Visualizer.views.home', name='home'),
    # url(r'^Visualizer/', include('Visualizer.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
