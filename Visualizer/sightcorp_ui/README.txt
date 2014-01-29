This document contains notes of things that may be useful for configuring the project.
Further information (e.g., system architecture) can be found in the folder ./docs, and in the document D2.5: http://groups.inf.ed.ac.uk/f4k/DELIVERABLES/D2.5.pdf

1. In case virtual environment is needed, e.g., in order to use different versions of python, django, etc. Do the following:

 - Assume the version is installed under virtualenv_django1.4
 - include system installed packages:
   e.g. virtualenv  --system-site-packages virtualenv_django1.4/
 - activate the virtual environment:
   e.g. source virtualenv_django1.4/bin/activate

2. run the django-admin.py to start up a project:
If virtural environment is used as described in 1., django-admin.py is run under the virtualenv_django1.4/

3. Database:
You need to connect to the database, which will be made public on April 2014. 
The database parameters must be filled in the file /django_ui/settings.py

4. project vs. app
 - the project is django_ui
 - f4k_ui is an app; an app can live in anywhere in the python path, e.g., if we create it next to manage.py, then it is a top-level module, instead of a sub-module of django_ui

5. When deploying:
 - copy the admin files to static, somehow it doesn't work if we don't do it
 - in wsgi.py, include the project directory in the sys path

