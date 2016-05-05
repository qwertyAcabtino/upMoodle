import json

from rest.models import User, ErrorMessage
from rest.models.message.errorMessage import ErrorMessageType
from tests.integration.system import CookiesTestCase
from tests.utils import load_fixture, assert_error_response


class SignUpTestCase(CookiesTestCase):

    def setUp(self):
        super(SignUpTestCase, self).setUp()
        load_fixture("provision-data")

    def test_basic_signup(self):
        response = self.client.post(
            '/auth/signup/',
            data={'email': 'test@eui.upm.es', 'password': '12341234', 'nick': 'vipvip', 'name': 'vip vip'})
        decoded = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(decoded['userId'], 1)
        self.assertEqual(len(User.objects.all()), 1)

    def test_duplicate_email(self):
        response = self.client.post('/auth/signup/',
                                    {'email': 'test112312@eui.upm.es', 'password': 'qqwerwerqwere',
                                     'nick': 'vqweripasdfvip', 'name': 'vip vip'})
        response = self.client.post('/auth/signup/',
                                    {'email': 'test112312@eui.upm.es', 'password': 'qqwerwerqwere',
                                     'nick': 'vqweripasdfvip', 'name': 'vip vip'})
        self.assertEqual(response.status_code, 400)
        decoded = json.loads(response.content)
        self.assertIsNotNone(decoded['error'])
        self.assertEqual(len(User.objects.all()), 1)

    def test_1_invalid_email(self):
        response = self.client.post('/auth/signup/',
                                    {'email': 'test112@google.com', 'password': 'qqwerwerqwere',
                                     'nick': 'vqwsdfsdferipvip', 'name': 'vip vip'})
        self.assertEqual(len(User.objects.all()), 0)
        assert_error_response(response, ErrorMessageType.EMAIL_INVALID)

    def test_duplicate_nick(self):
        response = self.client.post('/auth/signup/',
                                    {'email': 'viperey@eui.upm.es', 'password': '12341234', 'nick': 'vipvip',
                                     'name': 'vip vip'})
        response = self.client.post('/auth/signup/',
                                    {'email': 'viperey@eui.upm.es', 'password': '12341234', 'nick': 'vipvip',
                                     'name': 'vip vip'})
        assert_error_response(response, ErrorMessageType.INCORRECT_DATA)
        self.assertEqual(len(User.objects.all()), 1)

    def test_password_length(self):
        response = self.client.post('/auth/signup/', {'email': 'viperey@eui.upm.es', 'password': 'qwer', 'nick': 'vipvip',
                                                 'name': 'vip vip'})
        assert_error_response(response, ErrorMessageType.PASSWORD_LENGTH)
        self.assertEqual(len(User.objects.all()), 0)

    def test_password_length_2(self):
        response = self.client.post('/auth/signup/', {'email': 'viperey@eui.upm.es',
                                                 'password': 'qwerwqwerqwqwerqwqwerqwqwerqwqwerqwqwerqwqwerqwqwerqwqwerqwqwerqwqwerqwqwerqwqwerqwqwerqwqwerqwqwqwer',
                                                 'nick': 'vipvip', 'name': 'vip vip'})
        self.assertEqual(len(User.objects.all()), 0)
        assert_error_response(response, ErrorMessageType.PASSWORD_LENGTH)

    def test_nick_length(self):
        response = self.client.post('/auth/signup/',
                                    {'email': 'viperey@eui.upm.es', 'password': 'qwerqwerqwer', 'nick': 'qwe',
                                     'name': 'vip vip'})
        self.assertEqual(len(User.objects.all()), 0)
        assert_error_response(response, ErrorMessageType.NICK_LENGTH)

    def test_nick_length_2(self):
        response = self.client.post('/auth/signup/', {'email': 'viperey@eui.upm.es', 'password': 'qwerqwerqwer',
                                                 'nick': 'qweqweqweqweqweqweqweqwe', 'name': 'vip vip'})
        self.assertEqual(len(User.objects.all()), 0)
        assert_error_response(response, ErrorMessageType.NICK_LENGTH)

    def test_none_field_email(self):
        response = self.client.post('/auth/signup/', {'email': '', 'password': 'qwerqwerqwer', 'nick': 'qweqwerqw'})
        assert_error_response(response, ErrorMessageType.INCORRECT_DATA)

    def test_none_field_email_2(self):
        response = self.client.post('/auth/signup/', {'password': 'qwerqwerqwer', 'nick': 'qweqwerqw'})
        assert_error_response(response, ErrorMessageType.INCORRECT_DATA)

    def test_none_field_password(self):
        response = self.client.post('/auth/signup/', {'email': 'viperey@eui.upm.es', 'password': '', 'nick': 'qweqweqwer'})
        assert_error_response(response, ErrorMessageType.INCORRECT_DATA)

    def test_none_field_password_2(self):
        response = self.client.post('/auth/signup/', {'email': 'viperey@eui.upm.es', 'nick': 'qweqweqwer'})
        assert_error_response(response, ErrorMessageType.INCORRECT_DATA)

    def test_none_field_nick(self):
        response = self.client.post('/auth/signup/', {'email': 'viperey@eui.upm.es', 'password': 'qwerqwerqwer', 'nick': ''})
        assert_error_response(response, ErrorMessageType.INCORRECT_DATA)

    def test_none_field_nick_2(self):
        response = self.client.post('/auth/signup/', {'email': 'viperey@eui.upm.es', 'password': 'qwerqwerqwer'})
        assert_error_response(response, ErrorMessageType.INCORRECT_DATA)

    def test_none_field_2(self):
        response = self.client.post('/auth/signup/', {'email': 'viperey@eui.upm.es'})
        assert_error_response(response, ErrorMessageType.INCORRECT_DATA)

    def test_none_field_3(self):
        response = self.client.post('/auth/signup/', {})
        assert_error_response(response, ErrorMessageType.INCORRECT_DATA)
