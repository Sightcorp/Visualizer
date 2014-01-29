from django.shortcuts import render_to_response, redirect
from django.http import  HttpResponse
from django.core.context_processors import csrf
from django.template.context import RequestContext
from django.utils import simplejson
from django.views.decorators.cache import never_cache
import django_ui.settings as settings
import logging
from f4k_ui.db.models import Person, Source
from f4k_ui.parameters import VisualizationParameters
from f4k_ui.service.report import ReportService
from f4k_ui.service.video import VideoService
from f4k_ui.service.viz import VizService
from f4k_ui.service.filter import FilterService
from f4k_ui.service.workflow import WorkflowService

# The following lines are "not used" but needed...
#######################################################
species_names = [] #dict(Species.objects.get_species())

cameras_list = [] #Cameras.objects.get_cameras()
cameras_names = {
    'cameras_HoBiHu': ['%s' % c[0] for c in cameras_list if c[1] == 'HoBiHu'],
    'cameras_LanYu': ['%s' % c[0] for c in cameras_list if c[1] == 'LanYu'],
    'cameras_NPP3': ['%s' % c[0] for c in cameras_list if c[1] == 'NPP-3']
}

video_class_names = {'video_class_names': {
    1: 'Algae',
    2: 'Blurry',
    3: 'Complex',
    4: 'Discarded', #Encoding Error
    5: 'Very Blurry',
    6: 'Normal',
    7: 'Unknown'
}}
#######################################################

vizService = VizService(species_names)
filterService = FilterService(species_names, cameras_names)
videoService = VideoService(species_names)
workflowService = WorkflowService(cameras_list)

reportService = ReportService()

@never_cache
def visualization(request):
    """Default index page for the ui is the visualization page."""
    print 'visualization request 1'
    return process_request(request, 'vis', 'f4k_ui/visualization.html')

@never_cache
def videos(request):
    """Corresponds to video tab."""
    return process_request(request, 'vid', 'f4k_ui/videos.html')

@never_cache
def vidana(request):
    """Corresponds to video analysis tab."""
    return process_request(request, 'vidana', 'f4k_ui/vidana.html')

@never_cache
def rawdata(request):
    """Corresponds to rawdata tab."""
    return process_request(request, 'rawdata', 'f4k_ui/rawdata.html')

@never_cache
def report(request):
    """Corresponds to report tab."""
    return process_request(request, 'report', 'f4k_ui/report.html')

@never_cache
def home(request):
    """Corresponds to home page."""
    return process_request(request, 'home', 'f4k_ui/home.html')

@never_cache
def afterlogin(request):
    """Login redirection."""
    return redirect(settings.LOGIN_REDIRECT_URL)


def process_request(request, current_tab, template):
    """Process the request, update the context."""
    # TODO: the below can better be done by the wrapper @login_required and
    # setting the login_url (in settings, I believe), if it's not already done
    #if not request.user.is_authenticated():
    #    return redirect('%saccounts/login/' % settings.HOME_ROOT)

    logging.info("Requesting Page tab: '%s'" % current_tab)

    # TODO: this is ugly, there's a reverse_url function in django which
    # takes a name and optional arguments and returns the url. This is
    # better because if you would change your urls, nothing breaks.

    #urls for requesting data for main chart
    viz_data_url = '%s%s' % (settings.HOME_ROOT, 'ui/viz_data/')
    #urls for requesting data for filters
    filter_data_url = '%s%s' % (settings.HOME_ROOT, 'ui/filter_data/')
    #urls for requesting data for video list
    video_data_url = '%s%s' % (settings.HOME_ROOT, 'ui/video_data/')
    #urls for requesting data for user query management
    user_query_url = '%s%s' % (settings.HOME_ROOT, 'ui/user_query_data/')
    #urls for requesting data for report
    user_report = '%s%s' % (settings.HOME_ROOT, 'ui/user_report/')
    user_report_file = '%s%s' % (settings.HOME_ROOT, 'ui/user_report_file/')

    home_url = '%s%s' % (settings.HOME_ROOT, 'ui/home/')

    #update context
    c = {
        'user': request.user,
        'active_tab': current_tab,
        'active': {current_tab: 'active'},
        'viz_data_url': viz_data_url,
        'filter_data_url': filter_data_url,
        'video_data_url': video_data_url,
        'user_query_url': user_query_url,
        'user_report': user_report,
        'user_report_file': user_report_file,
        'home_url': home_url,
        }

    parameters = VisualizationParameters(request, species_names)
    c.update(parameters.status())
    c.update(video_class_names)

    c.update(csrf(request))
    response = render_to_response(template, c, context_instance=RequestContext(request))
    return response


def viz_data(request):
    """Handle request for data for visualization in zone B."""
    return serve_async_response(request, vizService)

def filter_data(request):
    """Handle request for filter data in zone D."""
    return serve_async_response(request, filterService)

def video_data(request):
    """Handle request for data for videos in zone B."""
    return serve_async_response(request, videoService)

@never_cache
def user_query_data(request):
    """Handle request for data for video analysis."""
    return serve_async_response(request, workflowService)

@never_cache
def user_report(request):
    """Handle request for data for user report."""
    return serve_async_response(request, reportService)

@never_cache
def user_report_file(request):
    return reportService.csv(request)

def serve_async_response(request, service):
    if request.is_ajax():
        data = service.process_request(request)
        json_data = simplejson.dumps(data)
        return HttpResponse(json_data, mimetype="application/json")
    else:
        logging.warn('This is NOT ajax request!')
        return render_to_response('403.html')
