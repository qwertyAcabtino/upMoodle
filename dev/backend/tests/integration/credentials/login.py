import json

from django.test import RequestFactory

from backend.settings import SESSION_COOKIE_NAME
from rest.MESSAGES_ID import *
from rest.models import User, ErrorMessage
from rest.routers import login
from tests.integration.system import AuthenticationTestBase
from tests.utils import load_fixture


class LoginTestCase(AuthenticationTestBase):

    def setUp(self):
        super(LoginTestCase, self).setUp()
        load_fixture("provision-data")
        self.createUser()

    def test_1_basic_login(self):
        response = self.client.post('/login/', {'email': 'test@eui.upm.es', 'password': '12341234'})
        self.assertEqual(response.status_code, 200)
        user = User.objects.get(email='test@eui.upm.es')
        self.assertTrue(user.confirmedEmail)

    def test_2_login_unconfirmed_email(self):
        user = User.objects.get(email='test@eui.upm.es')
        user.confirmedEmail = False
        user.save()
        response = self.client.post('/login/', {'email': 'test@eui.upm.es', 'password': '12341234'})
        self.assertEqual(response.status_code, 400)
        decoded = json.loads(response.content)
        self.assertEqual(ErrorMessage.objects.get(pk=UNCONFIRMED_EMAIL).error, decoded['error'])
        user = User.objects.get(email='test@eui.upm.es')
        user.confirmedEmail = True
        user.save()

    def test_3_login_empty_email(self):
        response = self.client.post('/login/', {'email': '', 'password': '12341234'})
        self.assertEqual(response.status_code, 400)
        decoded = json.loads(response.content)
        self.assertEqual(ErrorMessage.objects.get(pk=INCORRECT_DATA).error, decoded['error'])

    def test_4_login_empty_email_2(self):
        response = self.client.post('/login/', {'password': '12341234'})
        self.assertEqual(response.status_code, 400)
        decoded = json.loads(response.content)
        self.assertEqual(ErrorMessage.objects.get(pk=INCORRECT_DATA).error, decoded['error'])

    def test_5_login_empty_password(self):
        response = self.client.post('/login/', {'email': 'test@eui.upm.es', 'password': ''})
        self.assertEqual(response.status_code, 400)
        decoded = json.loads(response.content)
        self.assertEqual(ErrorMessage.objects.get(pk=INCORRECT_DATA).error, decoded['error'])

    def test_6_login_empty_password_2(self):
        response = self.client.post('/login/', {'email': 'test@eui.upm.es'})
        self.assertEqual(response.status_code, 400)
        decoded = json.loads(response.content)
        self.assertEqual(ErrorMessage.objects.get(pk=INCORRECT_DATA).error, decoded['error'])

    # In this case, for testing the behaviour when having cookies disabled, the request has to be made in a special way.
    def test_7_login_disabled_cookies(self):
        request = RequestFactory().post('/login/', {'email': 'test@eui.upm.es', 'password': '12341234'})
        request.COOKIES[SESSION_COOKIE_NAME] = None
        request.session = self.client.session
        request.session.TEST_COOKIE_VALUE = None

        response = login(request)
        self.assertEqual(response.status_code, 400)
        decoded = json.loads(response.content)
        self.assertEqual(ErrorMessage.objects.get(pk=DISABLED_COOKIES).error, decoded['error'])

    def test_8_login_disabled_cookies_2(self):
        request = RequestFactory().post('/login/', {'email': 'test@eui.upm.es', 'password': '12341234'})
        request.session = self.client.session
        request.COOKIES[SESSION_COOKIE_NAME] = None

        response = login(request)
        self.assertEqual(response.status_code, 400)
        decoded = json.loads(response.content)
        self.assertEqual(ErrorMessage.objects.get(pk=DISABLED_COOKIES).error, decoded['error'])

    def test_9_login_disabled_cookies_3(self):
        request = RequestFactory().post('/login/', {'email': 'test@eui.upm.es', 'password': '12341234'})
        request.session = self.client.session
        request.COOKIES[SESSION_COOKIE_NAME] = ''

        response = login(request)
        self.assertEqual(response.status_code, 400)
        decoded = json.loads(response.content)
        self.assertEqual(ErrorMessage.objects.get(pk=DISABLED_COOKIES).error, decoded['error'])
