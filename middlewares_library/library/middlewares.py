import time
import logging

from django.db import connection
from django.http import HttpResponseRedirect, HttpResponse

# from middlewares_library import settings
#  ^ This is wrong, because then I can't override the settings in my tests
#  http://stackoverflow.com/questions/28799803/overriding-settings-for-unit-tests-in-django-doesnt-work-properly
from django.conf import settings 
from library.models import RequestLog


# Get an instance of a logger
logger = logging.getLogger(__name__)


class RequestLoggingMiddleware(object):
    """
    Logs each request as a RequestLog model instance. The model will contain
    all details about the request, such as HTTP method, response status
    code, ip, GET and POST params, etc. Follow the fields described in
    the RequestLog model.
    """

    def process_request(self, request):
        self.start_time = time.time()
        self.db_connection = connection

    def process_response(self, request, response):
        # Clock the operation
        duration = time.time() - self.start_time
        
        if 'HTTP_USER_AGENT' in request.META:
            user_agent = request.META['HTTP_USER_AGENT']
        else:
            user_agent = None
            
        # Create the new instance
        RequestLog.objects.create(
            method=request.method,
            scheme=request.scheme,
            duration_in_seconds=duration,
            code=response.status_code,
            url=request.path,
            full_url=request.get_full_path(),
            abs_uri=request.build_absolute_uri(),
            ip=request.META['REMOTE_ADDR'],
            get_params=request.GET,
            user_agent=user_agent,
            query_count=len(self.db_connection.queries),
        )
        
        return response


class SSLRedirectMiddleware(object):
    """
    If the request is not using HTTPS, redirects to the same URL but
    using HTTPS.
    """
    # Check out request.is_secure()
    def process_request(self, request):
        # request.scheme = 'https' # Get an AttributeError: can't set attribute
        old_uri = request.build_absolute_uri()
        new_uri = 'https' + old_uri[old_uri.find('://'):]
        if old_uri != new_uri:
            return HttpResponseRedirect(new_uri)
    

class WWWRedirectMiddleware(object):
    """
    If "www" is included in the URL, redirects to the nacked version
    of the domain (without "www" at the beginning)
    """
    def process_request(self, request):
        old_uri = request.build_absolute_uri()
        uses_www = request_uses_www(old_uri)
        if uses_www and not settings.USE_WWW:
            return HttpResponseRedirect(old_uri.replace('://www.', '://'))
        if settings.USE_WWW and not uses_www:
            return HttpResponseRedirect(old_uri.replace('://', '://www.'))


class ExceptionLoggingMiddleware(object):
    """
    Writes a log entry for every exception raised in any request.
    """
    def process_exception(self, request, exception):
        logger.exception(str(exception))
        return HttpResponseRedirect('/')

def request_uses_www(url):
    """
    Returns a boolean that represents whether the url uses the www subdomain
    """
    subdomain = url.find('://')
    return url[subdomain+3:subdomain+7] == 'www.'