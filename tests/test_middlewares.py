from datetime import datetime
import logging
from testfixtures import LogCapture

from django.test import override_settings#, TestCase # Not sure I actually need WebTest for anything
from django_webtest import WebTest
from django.conf import settings
from django.contrib.auth.models import User

from library.models import RequestLog

import unittest # Take this out once I stop skipping tests


# class MiddlewaresTestCase(TestCase):
class MiddlewaresTestCase(WebTest):

    def setUp(self):
        super(MiddlewaresTestCase, self).setUp()
        self.user = User.objects.create_user(
            username='User', password='abc123', is_staff=True, is_superuser=True)

    def tearDown(self):
        RequestLog.objects.all().delete()

    # @unittest.skip("testing skipping")
    @override_settings(USE_WWW=False)
    def test_request_logging_middleware(self):
        """Should create an instance of RequestLog for each request attended"""
        # Preconditions
        self.assertEqual(RequestLog.objects.count(), 0)
        
        self.client.login(username=self.user.username, password='abc123')
        params = {'foo': 'bar'}
        self.client.get('/admin/', params, secure=True, follow=True)
        # self.client.get('/admin/', params, follow=True)

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

    @override_settings(USE_WWW=False)
    def test_ssl_redirect_middleware(self):
        """Should redirect any request not using HTTPS to the same URL over HTTPS"""
        # Preconditions
        self.assertEqual(RequestLog.objects.count(), 0)
        
        self.client.login(username=self.user.username, password='abc123')
        response = self.client.get('/admin/', secure=False, follow=True)
        
        # Postconditions
        self.assertEqual(RequestLog.objects.count(), 2)
        first_log = RequestLog.objects.first()
        last_log = RequestLog.objects.last()
        self.assertEqual(first_log.scheme, 'http')
        self.assertEqual(last_log.scheme, 'https')
        self.assertEqual(first_log.code, 302)
        self.assertEqual(first_log.full_url, last_log.full_url)

    @override_settings(USE_WWW=True)
    def test_www_redirect_with_use_www(self):
        """
        Should redirect any request without the www subdomain to the same url
        with the www subdomain
        """
        # Preconditions
        self.assertEqual(RequestLog.objects.count(), 0)
        
        self.client.login(username=self.user.username, password='abc123')
        
        self.client.get(
            '/admin/', 
            SERVER_NAME='testserver', # http://stackoverflow.com/a/6291428/3697120
            secure=True,
            follow=True
        )
        
        # Postconditions
        self.assertEqual(RequestLog.objects.count(), 2)
        first_log = RequestLog.objects.first()
        last_log = RequestLog.objects.last()
        self.assertEqual(first_log.code, 302)
        self.assertIn('www.', last_log.abs_uri)
        self.assertEqual(first_log.full_url, last_log.full_url)
        
        self.client.get(
            '/admin/',
            SERVER_NAME="www.testserver", 
            secure=True,
            follow=True
        )
        
        # Postconditions
        self.assertEqual(RequestLog.objects.count(), 3)
        last_log = RequestLog.objects.last()
        self.assertIn('www.', last_log.abs_uri)

    @override_settings(USE_WWW=False)
    def test_www_redirect_with_not_use_www(self):
        """
        Should redirect any request using the www subdomain to the same url
        without it
        """
        # Preconditions
        self.assertEqual(RequestLog.objects.count(), 0)
        
        self.client.login(username=self.user.username, password='abc123')
        
        self.client.get(
            '/admin/',
            SERVER_NAME="www.testserver",
            secure=True,
            follow=True
        )
        
        # Postconditions
        self.assertEqual(RequestLog.objects.count(), 2)
        first_log = RequestLog.objects.first()
        last_log = RequestLog.objects.last()
        self.assertEqual(first_log.code, 302)
        self.assertNotIn('www.', last_log.abs_uri)
        self.assertEqual(first_log.full_url, last_log.full_url)
        
        self.client.get(
            '/admin/',
            SERVER_NAME="testserver",
            secure=True,
            follow=True
        )
        
        # Postconditions
        self.assertEqual(RequestLog.objects.count(), 3)
        last_log = RequestLog.objects.last()
        self.assertNotIn('www.', last_log.abs_uri)
    
    @override_settings(USE_WWW=False)
    def test_exception_logging_middleware(self):
        """Should do something for every request that raises an exception"""
        # Preconditions
        self.assertEqual(RequestLog.objects.count(), 0)
        
        self.client.login(username=self.user.username, password='abc123')
        
        # No exception should be logged
        with LogCapture(level=logging.ERROR) as log_cap_1:
            logger = logging.getLogger('test1')
            self.client.get(
                '/invalid_url/',
                SERVER_NAME="testserver",
                secure=True,
                follow=True
            )
        
        # An exception should be logged
        with LogCapture(level=logging.ERROR) as log_cap_2:
            logger = logging.getLogger('test2')
            self.client.get(
                '/view_raises_exception/',
                SERVER_NAME="testserver",
                secure=True,
                follow=True
            )
        
        # No exception should be logged
        with LogCapture(level=logging.ERROR) as log_cap_3:
            logger = logging.getLogger(__name__)
            self.client.get(
                '/view_raises_no_exceptions/',
                SERVER_NAME="testserver",
                secure=True,
                follow=True
            )
        
        # Postconditions
        # Log caps 1 & 3 should not have logged an exception.  2 should have.
        log_cap_1.check()
        log_cap_2.check(('library.middlewares', 'ERROR', 'Custom error message...'),)
        log_cap_3.check()