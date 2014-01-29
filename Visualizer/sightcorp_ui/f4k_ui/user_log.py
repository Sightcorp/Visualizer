import logging
import threading


_thread_local = threading.local()


def set_request(req):
    _thread_local.current_django_request = req


def get_request():
    return getattr(_thread_local, 'current_django_request', None)


class StoreRequestMiddleware(object):
    def process_request(self, request):
        set_request(request)

class UserFilter(logging.Filter):
    def filter(self, record):
        record.username = ''
        request = get_request()
        if hasattr(request,'user'):
            record.username = request.user.username

        return 1
