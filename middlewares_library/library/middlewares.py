from .models import ExceptionLog, RequestLog
from django.db import connection
from django.http import HttpResponseRedirect

import datetime
from math import floor
from urlparse import urlparse

class RequestLoggingMiddleware(object):
    """
    Logs each request as a RequestLog model instance. The model will contain
    all details about the request, such as HTTP method, response status
    code, ip, GET and POST params, etc. Follow the fields described in
    the RequestLog model.
    """
    def process_request(self, request):
        self.request_time = datetime.datetime.now()

    def process_response(self, request, response):
        duration = floor((datetime.datetime.now() - self.request_time).total_seconds())
        
        queries_number = len(connection.queries)
        
        parameters = request.GET.dict()
        
        if 'HTTP_USER_AGENT' in request.META:
            browser = request.META['HTTP_USER_AGENT']
        else:
            browser = None
            
        logged_request = RequestLog.objects.create(
            #timestamp = models.DateTimeField(auto_now_add=True)
            method = request.method,
            duration_in_seconds = duration,
            code = response.status_code,
            url = request.path,
            full_url = request.get_full_path(),
            ip = request.META['REMOTE_ADDR'],
            get_params = parameters,
            user_agent = browser,
            query_count = queries_number
            )
        # print(request.GET.dict())
        logged_request.save()
        return response
        

class SSLRedirectMiddleware(object):
    """
    If the request is not using HTTPS, redirects to the same URL but
    using HTTPS.
    """
    def process_response(self, request, response):
        if not request.is_secure():
            return HttpResponseRedirect('https://' + request.META['HTTP_HOST'] + str(request.get_full_path()))
        return response
        

class WWWRedirectMiddleware(object):
    """
    If "www" is included in the URL, redirects to the nacked version
    of the domain (without "www" at the beginning)
    """
    def process_request(self, request):
        original_url = request.build_absolute_uri(request.get_full_path())
        url_parsed = urlparse(original_url)
        nacked_url = url_parsed.netloc[4:] 
        print(url_parsed.netloc)
        print(nacked_url)
        if "www" in url_parsed.netloc:
            print(url_parsed.scheme + '://' + nacked_url + url_parsed.path)
            print(request.META['HTTP_HOST'])
            request.META['HTTP_HOST'] = url_parsed.scheme + '://' + nacked_url + url_parsed.path
            print("FINAL: " + request.META['HTTP_HOST'])
            return HttpResponseRedirect(url_parsed.scheme + '://' + nacked_url + url_parsed.path)
        # print(request.build_absolute_uri(request.get_full_path()))

class ExceptionLoggingMiddleware(object):
    """
    Writes a log entry for every exception raised in any request.
    """
    def process_exception(self, request, exception):
        exception_logged = ExceptionLog.objects.create(type_of_exception=str(type(exception)), location=request.path)
        exception_logged.save()
