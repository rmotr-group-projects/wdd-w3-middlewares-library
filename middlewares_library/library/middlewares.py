class RequestLoggingMiddleware(object):
    """
    Logs each request as a RequestLog model instance. The model will contain
    all details about the request, such as HTTP method, response status
    code, ip, GET and POST params, etc. Follow the fields described in
    the RequestLog model.
    """

    def process_request(self, request):
        pass

    def process_response(self, request, response):
        pass


class SSLRedirectMiddleware(object):
    """
    If the request is not using HTTPS, redirects to the same URL but
    using HTTPS.
    """
    pass


class WWWRedirectMiddleware(object):
    """
    If "www" is included in the URL, redirects to the nacked version
    of the domain (without "www" at the beginning)
    """
    pass


class ExceptionLoggingMiddleware(object):
    """
    Writes a log entry for every exception raised in any request.
    """
    pass
