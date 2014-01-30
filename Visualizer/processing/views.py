from database.models import *
from forms import *
#from processing.tasks import *

import datetime

from django.http                  import HttpResponse
from django.shortcuts             import render
from django.utils                 import simplejson
from django.views.decorators.csrf import csrf_exempt


#import sys

# Utils

# Wrapper to handle server errors. The client should always receive an answer
def ma_error( view_func ):
  def wrapper( request, *args, **kwargs ):
    try:
      return view_func( request, *args, **kwargs )
    except Exception, e:
      json_response = {}
      json_response[ 'code' ]  = 1
      json_response[ 'description' ] = 'Server internal error: ' + str( e )
      #print >> sys.stderr, "Server error -------" # TODO : Diego : Remove
      #print >> sys.stderr, str( e ) # TODO : Diego : Remove
      #print >> sys.stderr, "-----------------------" # TODO : Diego : Remove
      return HttpResponse( simplejson.dumps( json_response, indent = 2 ), mimetype = "application/json" )
  return wrapper

# Utils End


@csrf_exempt
@ma_error
def start_session( request ):
  json_response = {}
  json_response[ 'code' ]  = 1
  json_response[ 'description' ] = 'Wrong request format'

  #print >> sys.stderr, " START SESSION REQUEST : ", repr(request.POST) # TODO : Diego : Remove

  if request.method == 'POST':
    start_session_form = StartSessionForm( request.POST )
    if start_session_form.is_valid():
      new_session = Session.objects.create( start_time = datetime.datetime.now(), id_source = start_session_form.source_model ) # TODO : Diego : Set client start_time if specified (feature request)
      json_response[ 'code' ] = 0
      json_response[ 'session_key' ]  = new_session.key
    else:
      json_response[ 'code' ] = 2
      json_response[ 'description' ] = "Invalid request"

  # The client's Json parser is expecting indentation!!!
  return HttpResponse( simplejson.dumps( json_response, indent = 2 ), mimetype = "application/json" )

@csrf_exempt
@ma_error
def stop_session( request ):
  json_response = {}
  json_response[ 'code' ]  = 1
  json_response[ 'description' ] = 'Wrong request format'

  #print >> sys.stderr, " STOP SESSION REQUEST : ", repr(request.POST) # TODO : Diego : Remove

  if request.method == 'POST':
    stop_session_form = StopSessionForm( request.POST )
    if stop_session_form.is_valid():
      stop_session_form.session_model.end_time = datetime.datetime.now() # TODO : Diego : Set client end_time if specified (feature request)
      stop_session_form.session_model.save()
      for person in stop_session_form.session_model.person_set.all():
          backgound_processing.delay( person )
      # TODO : Diego : Trigger Person_img processing for this session
      json_response[ 'code' ] = 0
    else:
      json_response[ 'code' ] = 2
      json_response[ 'description' ] = "Invalid request"

  # The client's Json parser is expecting indentation!!!
  return HttpResponse( simplejson.dumps( json_response, indent = 2 ), mimetype = "application/json" )


@csrf_exempt
@ma_error
def person_detection( request ):
  json_response = {}
  json_response[ 'code' ] = 1
  json_response[ 'description' ] = 'Wrong request format'

  #print >> sys.stderr, " PERSON DETECTION REQUEST : ", repr(request.POST) # TODO : Diego : Remove

  if request.method == 'POST':
    person_detection_form = PersonDetectionForm( request.POST )
    if person_detection_form.is_valid():
      new_person_detection = person_detection_form.save( commit = False )
      new_person_detection.id_person = person_detection_form.person_model # TODO : Diego : Check if it requires person_model.id_person
      new_person_detection.save()
      json_response[ 'code' ] = 0
    else:
      json_response[ 'code' ] = 2
      json_response[ 'description' ] = person_detection_form.get_validation_error() #"Invalid request" # TODO : Diego : report error description

  # The client's Json parser is expecting indentation!!!
  return HttpResponse( simplejson.dumps( json_response, indent = 2 ), mimetype = "application/json" )

@ma_error
def trigger_processing( request ):
  json_response = {}
  json_response[ 'code' ] = 0
  open_sessions = Session.objects.filter( end_time = None )
  for session in open_sessions:
    for p in session.person_set.all():
      backgound_processing.delay( p )

  return HttpResponse( simplejson.dumps( json_response, indent = 2 ), mimetype = "application/json" )
