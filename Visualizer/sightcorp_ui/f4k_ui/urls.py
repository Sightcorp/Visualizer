from django.conf.urls import patterns
from django.views.generic.base import RedirectView

urlpatterns = patterns('f4k_ui.views',
    (r'^$', RedirectView.as_view(url='home', permanent=True)),
    (r'^home/$', 'home'),
    (r'^videos/$', 'videos'),
    (r'^vidana/$', 'vidana'),
    (r'^rawdata/$', 'rawdata'),
    (r'^visualization/$', 'visualization'),
    (r'^report/$', 'report'),
    (r'^viz_data/$', 'viz_data'),
    (r'^filter_data/$', 'filter_data'),
    (r'^video_data/$', 'video_data'),
    (r'^user_query_data/$', 'user_query_data'),
    (r'^user_report/$', 'user_report'),
    (r'^user_report_file/$', 'user_report_file')
)