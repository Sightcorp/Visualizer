"""
WSGI config for django_ui project.

This module contains the WSGI application used by Django's development server
and any production WSGI deployments. It should expose a module-level variable
named ``application``. Django's ``runserver`` and ``runfcgi`` commands discover
this application via the ``WSGI_APPLICATION`` setting.

Usually you will have the standard Django WSGI application here, but it also
might make sense to replace the whole Django WSGI application with a custom one
that later delegates to the Django one. For example, you could introduce WSGI
middleware here, or combine a Django application with an application of another
framework.

"""
import os
import sys

#if this path is set here, we don't need to set WSGIPythonPath in httpd.conf
path = os.path.dirname(os.path.realpath(__file__)).rsplit(os.sep, 1)[0]
sys.path.append(path)

#os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
os.environ["DJANGO_SETTINGS_MODULE"]="django_ui.settings"

# This application object is used by any WSGI server configured to use this
# file. This includes Django's development server, if the WSGI_APPLICATION
# setting points here.
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

# Apply WSGI middleware here.
# from helloworld.wsgi import HelloWorldApplication
# application = HelloWorldApplication(application)
