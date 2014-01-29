from django_ui import settings

def inject_settings(request):
    return {'show_registration': settings.SHOW_REGISTRATION}