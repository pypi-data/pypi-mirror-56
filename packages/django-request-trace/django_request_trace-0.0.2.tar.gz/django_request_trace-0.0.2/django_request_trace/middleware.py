from uuid import uuid4

from django.conf import settings
from threading import current_thread
_trace_ids = {}

def get_current_trace_id():
    return _trace_ids.get(current_thread())


def set_trace_id(trace_id):
    _trace_ids[current_thread()] = trace_id;


def clear_trace_id():
    del _trace_ids[current_thread()]


def generate_trace_id():
    return str(uuid4())


def get_trace_id(request):
    trace_id = request.META.get('HTTP_X_TRACE_ID')
    if trace_id:
        return trace_id

    trace_id = request.META.get('HTTP_X_AMZN_TRACE_ID')
    if trace_id:
        return trace_id

    return generate_trace_id()


class TraceIdMiddleware(object):
    def __init__(self, get_response=None):
        self.get_response = get_response

    def __call__(self, request):
        request.trace_id = get_trace_id(request)
        set_trace_id(request.trace_id)
        response = self.get_response(request)
        clear_trace_id()
        return response

