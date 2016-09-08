import time
import logging

from django.db import connection
from django.utils.encoding import smart_str
from django.http import HttpResponseRedirect

from library.models import RequestLog

logger = logging.getLogger(__name__)


class RequestLoggingMiddleware(object):
    """
    Logs each request as a RequestLog model instance. The model will contain
    all details about the request, such as HTTP method, response status
    code, ip, GET and POST params, etc. Follow the fields described in
    the RequestLog model.
    """

    def process_request(self, request):
        request._start = time.time()

    def process_response(self, request, response):
        RequestLog.objects.create(
            method=request.method,
            duration_in_seconds=int(time.time() - request._start),
            code=response.status_code,
            url=smart_str(request.path_info),
            full_url=smart_str(request.get_full_path()),
            ip=request.META.get('REMOTE_ADDR'),
            get_params=request.GET.dict(),
            user_agent=request.META.get('HTTP_USER_AGENT'),
            query_count=len(connection.queries),
        )
        return response


class SSLRedirectMiddleware(object):

    def process_request(self, request):
        if not request.is_secure():
            url = 'https://127.0.0.1{}'.format(request.get_full_path())
            return HttpResponseRedirect(url)
        return None


class ExceptionLoggingMiddleware(object):

    def process_exception(self, request, exception):
        logger.error('Something went wrong, got: {}'.format(str(exception)))
