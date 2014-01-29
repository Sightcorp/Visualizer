from celery import task
from database.models import *

@task()
def backgound_processing( person ):
    person.compute_averages()
    return None

