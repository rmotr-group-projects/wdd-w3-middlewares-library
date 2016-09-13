from .models import ExceptionLog, RequestLog
from django.db import connection
from django.http import HttpResponseRedirect

import datetime
from math import floor

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
    # def process_request(self, request):
        # print("SSL: " + request.scheme)
        # print('HTTP_HOST' in request.META)
        # print(request.META['HTTP_HOST'])
        # if not request.is_secure():
        #     print(request.scheme + "://" + request.META['HTTP_HOST'] + str(request.get_full_path()))
        #     print('https://' + request.META['HTTP_HOST'] + str(request.get_full_path()))
        #     return HttpResponseRedirect('https://' + request.META['HTTP_HOST'] + str(request.get_full_path()))
    #     print(request.scheme)
    #     print(request.is_secure())
    #     if request.scheme == 'http':
    #         print("HTTP")
    #     else:
    #         print("something else")
    
    def process_response(self, request, response):
        print(request.scheme)
        print(request.is_secure())
        if not request.is_secure():
            print(request.scheme + "://" + request.META['HTTP_HOST'] + str(request.get_full_path()))
            print('https://' + request.META['HTTP_HOST'] + str(request.get_full_path()))
            return HttpResponseRedirect('https://' + request.META['HTTP_HOST'] + str(request.get_full_path()))
        return response
    #     if not request.is_secure():
    #     # print("SCHEME: " + request.scheme)
    #     # print("IS_SECURE: " + str(request.is_secure()))
    #     # if request.scheme == 'http':
    #     #     print("HTTP")
    #     # else:
    #     #     print("something else")
    #     # print(request.META['HTTP_X_FORWARDED_PROTO'])
    #     # if request.META:
    #     #     for i in request.META:
    #     #         print(i)
    #     #print('https://' + request.META['HTTP_HOST'] + str(request.get_full_path()))
    #     #return response
    #     # if 'HTTP_X_FORWARDED_PROTO' in request.META:
    #     #     if request.META['HTTP_X_FORWARDED_PROTO'] == 'http':
    #     #         # print(str(request.get_full_path()))
    #     #         # print("HTTP: " + request.META['HTTP_HOST'])
    #     #         # print('https://' + request.META['HTTP_HOST'] + str(request.get_full_path()))
                
    #     #         print("init")
    #     #         print("PROTO1: " + request.META['HTTP_X_FORWARDED_PROTO'])
    #         return HttpResponseRedirect('https://' + request.META['HTTP_HOST'] + str(request.get_full_path()))
    #     #         # return HttpResponseRedirect(request.build_absolute_uri(request.get_full_path()))
    #     #     print("PROTO2: " + request.META['HTTP_X_FORWARDED_PROTO'])
    #     return response
        
    


class WWWRedirectMiddleware(object):
    """
    If "www" is included in the URL, redirects to the nacked version
    of the domain (without "www" at the beginning)
    """
    # def process_request(self, request):
    #     print(request.build_absolute_uri(request.get_full_path()))
    pass

class ExceptionLoggingMiddleware(object):
    """
    Writes a log entry for every exception raised in any request.
    """
    # def process_request(self,request):
    #     print("works")
    
    def process_exception(self, request, exception):
        exception_logged = ExceptionLog.objects.create(type_of_exception=str(type(exception)), location=request.path)
        exception_logged.save()
        # print("Logged")
        # print(request)
        # print(str(type(exception)))
