import logging

from django_request_trace.middleware import get_current_trace_id


class TraceIdFilter(logging.Filter):
    def filter(self, record):
        record.trace_id = get_current_trace_id()
        return True