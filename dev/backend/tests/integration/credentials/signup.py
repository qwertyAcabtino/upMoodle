import json

from rest.MESSAGES_ID import EMAIL_INVALID, NICK_LENGTH, PASSWORD_LENGTH
from rest.models import User, ErrorMessage
from tests.integration.system import CookiesTestCase
from tests.utils import load_fixture


class SignUpTestCase(CookiesTestCase):

    def setUp(self):
        super(SignUpTestCase, self).setUp()
        load_fixture("provision-data")

    def test_basic_signup(self):
        response = self.client.post('/signup/',
                                    {'email': 'test@eui.upm.es', 'password': '12341234', 'nick': 'vipvip',
                                     'name': 'vip vip'})
        decoded = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(decoded['userId'], 1)
        self.assertEqual(len(User.objects.all()), 1)

    def test_duplicate_email(self):
        response = self.client.post('/signup/',
                                    {'email': 'test112312@eui.upm.es', 'password': 'qqwerwerqwere',
                                     'nick': 'vqweripasdfvip', 'name': 'vip vip'})
        response = self.client.post('/signup/',
                                    {'email': 'test112312@eui.upm.es', 'password': 'qqwerwerqwere',
                                     'nick': 'vqweripasdfvip', 'name': 'vip vip'})
        self.assertEqual(response.status_code, 400)
        decoded = json.loads(response.content)
        self.assertIsNotNone(decoded['error'])
        self.assertEqual(len(User.objects.all()), 1)

    def test_1_invalid_email(self):
        response = self.client.post('/signup/',
                                    {'email': 'test112@google.com', 'password': 'qqwerwerqwere',
                                     'nick': 'vqwsdfsdferipvip', 'name': 'vip vip'})
        self.assertEqual(response.status_code, 400)
        decoded = json.loads(response.content)
        self.assertIsNotNone(decoded['error'])
        self.assertEqual(len(User.objects.all()), 0)
        self.assertEqual(ErrorMessage.objects.get(pk=EMAIL_INVALID).error, decoded['error'])

    def test_duplicate_nick(self):
        response = self.client.post('/signup/',
                                    {'email': 'viperey@eui.upm.es', 'password': '12341234', 'nick': 'vipvip',
                                     'name': 'vip vip'})
        response = self.client.post('/signup/',
                                    {'email': 'viperey@eui.upm.es', 'password': '12341234', 'nick': 'vipvip',
                                     'name': 'vip vip'})
        self.assertEqual(response.status_code, 400)
        decoded = json.loads(response.content)
        self.assertIsNotNone(decoded['error'])
        self.assertEqual(len(User.objects.all()), 1)

    def test_password_length(self):
        response = self.client.post('/signup/', {'email': 'viperey@eui.upm.es', 'password': 'qwer', 'nick': 'vipvip',
                                                 'name': 'vip vip'})
        self.assertEqual(response.status_code, 400)
        decoded = json.loads(response.content)
        self.assertIsNotNone(decoded['error'])
        self.assertEqual(len(User.objects.all()), 0)
        self.assertEqual(ErrorMessage.objects.get(pk=PASSWORD_LENGTH).error, decoded['error'])

    def test_password_length_2(self):
        response = self.client.post('/signup/', {'email': 'viperey@eui.upm.es',
                                                 'password': 'qwerwqwerqwqwerqwqwerqwqwerqwqwerqwqwerqwqwerqwqwerqwqwerqwqwerqwqwerqwqwerqwqwerqwqwerqwqwerqwqwqwer',
                                                 'nick': 'vipvip', 'name': 'vip vip'})
        self.assertEqual(response.status_code, 400)
        decoded = json.loads(response.content)
        self.assertIsNotNone(decoded['error'])
        self.assertEqual(len(User.objects.all()), 0)
        self.assertEqual(ErrorMessage.objects.get(pk=PASSWORD_LENGTH).error, decoded['error'])

    def test_nick_length(self):
        response = self.client.post('/signup/',
                                    {'email': 'viperey@eui.upm.es', 'password': 'qwerqwerqwer', 'nick': 'qwe',
                                     'name': 'vip vip'})
        self.assertEqual(response.status_code, 400)
        decoded = json.loads(response.content)
        self.assertIsNotNone(decoded['error'])
        self.assertEqual(len(User.objects.all()), 0)
        self.assertEqual(ErrorMessage.objects.get(pk=NICK_LENGTH).error, decoded['error'])

    def test_nick_length_2(self):
        response = self.client.post('/signup/', {'email': 'viperey@eui.upm.es', 'password': 'qwerqwerqwer',
                                                 'nick': 'qweqweqweqweqweqweqweqwe', 'name': 'vip vip'})
        self.assertEqual(response.status_code, 400)
        decoded = json.loads(response.content)
        self.assertIsNotNone(decoded['error'])
        self.assertEqual(len(User.objects.all()), 0)
        self.assertEqual(ErrorMessage.objects.get(pk=NICK_LENGTH).error, decoded['error'])

    def test_none_field_email(self):
        response = self.client.post('/signup/', {'email': '', 'password': 'qwerqwerqwer', 'nick': 'qweqwerqw'})
        self.assertEqual(response.status_code, 400)

    def test_none_field_email_2(self):
        response = self.client.post('/signup/', {'password': 'qwerqwerqwer', 'nick': 'qweqwerqw'})
        self.assertEqual(response.status_code, 400)

    def test_none_field_password(self):
        response = self.client.post('/signup/', {'email': 'viperey@eui.upm.es', 'password': '', 'nick': 'qweqweqwer'})
        self.assertEqual(response.status_code, 400)

    def test_none_field_password_2(self):
        response = self.client.post('/signup/', {'email': 'viperey@eui.upm.es', 'nick': 'qweqweqwer'})
        self.assertEqual(response.status_code, 400)

    def test_none_field_nick(self):
        response = self.client.post('/signup/', {'email': 'viperey@eui.upm.es', 'password': 'qwerqwerqwer', 'nick': ''})
        self.assertEqual(response.status_code, 400)

    def test_none_field_nick_2(self):
        response = self.client.post('/signup/', {'email': 'viperey@eui.upm.es', 'password': 'qwerqwerqwer'})
        self.assertEqual(response.status_code, 400)

    def test_none_field_2(self):
        response = self.client.post('/signup/', {'email': 'viperey@eui.upm.es'})
        self.assertEqual(response.status_code, 400)

    def test_none_field_3(self):
        response = self.client.post('/signup/', {})
        self.assertEqual(response.status_code, 400)
