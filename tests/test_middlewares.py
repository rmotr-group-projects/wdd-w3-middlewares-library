from datetime import datetime
from testfixtures import LogCapture

from django.test import TestCase
from django.conf import settings
from django.contrib.auth.models import User

from library.models import RequestLog, ExceptionLog


class MiddlewaresTestCase(TestCase):

    def setUp(self):
        super(MiddlewaresTestCase, self).setUp()
        self.user = User.objects.create_user(
            username='User', password='abc123', is_staff=True, is_superuser=True)

    def tearDown(self):
        RequestLog.objects.all().delete()

    def test_request_login_middleware(self):
        """Should create an instance of RequestLog for each request attended"""
        # Preconditions
        self.assertEqual(RequestLog.objects.count(), 0)

        self.client.login(username=self.user.username, password='abc123')
        params = {'foo': 'bar'}
        self.client.get('/admin/', params, follow=True, secure=True, HTTP_HOST='example.com')

        # Postconditions
        self.assertEqual(RequestLog.objects.count(), 1)
        log = RequestLog.objects.first()
        self.assertEqual(log.method, 'GET')
        self.assertEqual(log.code, 200)
        self.assertEqual(log.url, '/admin/')
        self.assertEqual(log.full_url, '/admin/?foo=bar')
        self.assertEqual(log.ip, '127.0.0.1')
        self.assertEqual(log.get_params, {'foo': 'bar'})
        self.assertEqual(log.user_agent, None)
        self.assertEqual(log.query_count, 0)
        self.assertTrue(isinstance(log.timestamp, datetime))
        self.assertTrue(isinstance(log.duration_in_seconds, int))

    def test_page_with_no_exception(self):
        """Pages with no exception are ignored by the middleware"""
        # Preconditions
        self.assertEqual(ExceptionLog.objects.count(), 0)
        
        self.client.login(username=self.user.username, password='abc123')
        params = {}
        #self.client.get('/admin/', params, follow=True, secure=True)
        self.client.get('/no-exception/', follow=True, secure=True, HTTP_HOST='example.com')
        
        # Postconditions
        self.assertEqual(ExceptionLog.objects.count(), 0)
    
    def test_page_with_exception(self):
        """Pages with exception are stored in a model"""
        # Preconditions
        self.assertEqual(ExceptionLog.objects.count(), 0)
        
        self.client.login(username=self.user.username, password='abc123')
        params = {}
        # self.client.get('/admin/', params, follow=True, secure=True, HTTP_HOST='example.com')
        try:
            self.client.get('/exception', secure=True, HTTP_HOST='example.com') #follow=True, 
        except:
            self.assertEqual(ExceptionLog.objects.count(), 1)
        
        # Postconditions
        first_log = ExceptionLog.objects.first()
        self.assertEqual(first_log.type_of_exception, "<type 'exceptions.ValueError'>")
        self.assertEqual(first_log.location, "/exception")
    
    def test_http_redirect_https(self):
        """If the requested URL uses HTTP, redirect the user to HTTPS-based URL"""
        # Preconditions
        response = self.client.get('/', secure=False, HTTP_HOST='example.com') #follow=True,
        
        # Postconditions
        self.assertEqual(response.status_code, 302)
    
    def test_https_no_redirect(self):
        """If the requested URL uses HTTPS, do not redirect"""
        # Preconditions
        response = self.client.get('/', secure=True, HTTP_HOST='example.com') #follow=True
        
        # Postconditions
        # test for http/https
        self.assertEqual(response.status_code, 200)
        
    def test_www_redirects(self):
        """If the requested URL is coming with WWW, redirect"""
        # Preconditions
        response = self.client.get('/', secure=True, HTTP_HOST='www.example.com')
        
        # Postconditions
        self.assertEqual(response.status_code, 302)
        print(response.client)
        self.assertEqual(response.request['HTTP_HOST'], 'example.com')
    
    def test_www_no_redirect(self):
        """If the requested URL is not coming with WWW, do not redirect"""
        # Preconditions
        response = self.client.get('/', secure=True, HTTP_HOST='example.com')
        
        # Postconditions
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.request['HTTP_HOST'], 'example.com')
        