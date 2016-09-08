from datetime import datetime
from testfixtures import LogCapture

from django.test import TestCase
from django.conf import settings
from django.contrib.auth.models import User

from library.models import RequestLog


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
        self.client.get('/admin/', params, follow=True)

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

    def test_ssl_redirect_middleware(self):
        """Should redirect to secure url when given url is insecure"""
        settings.MIDDLEWARE_CLASSES.append('library.middlewares.SSLRedirectMiddleware')
        response = self.client.get('http://127.0.0.1/test/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, 'https://127.0.0.1/test/')

    def test_exception_logging_middleware(self):
        """Should log all errors during the request/response lifecycle"""
        with self.assertRaises(ValueError):
            with LogCapture() as capture:
                self.client.get('/exception/', follow=True)
                capture.check(
                    ('library.middlewares', 'ERROR', 'Something went wrong!')
                )
