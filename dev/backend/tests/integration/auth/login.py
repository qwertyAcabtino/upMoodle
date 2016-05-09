from rest.models import User
from rest.models.message.errorMessage import ErrorMessage
from tests.integration.auth.system import AuthenticationTestBase
from tests.utils import load_fixture, assert_error_response


class LoginTestCase(AuthenticationTestBase):

    def setUp(self):
        super(LoginTestCase, self).setUp()
        load_fixture("provision-data")
        self.createUser()

    def test_1_basic_login(self):
        response = self.client.post('/auth/login/', {'email': 'test@eui.upm.es', 'password': '12341234'})
        self.assertEqual(response.status_code, 200)
        user = User.objects.get(email='test@eui.upm.es')
        self.assertTrue(user.confirmedEmail)

    def test_2_login_unconfirmed_email(self):
        user = User.objects.get(email='test@eui.upm.es')
        user.confirmedEmail = False
        user.save()
        response = self.client.post('/auth/login/', {'email': 'test@eui.upm.es', 'password': '12341234'})
        assert_error_response(response, ErrorMessage.Type.UNCONFIRMED_EMAIL)
        user = User.objects.get(email='test@eui.upm.es')
        user.confirmedEmail = True
        user.save()

    def test_3_login_empty_email(self):
        response = self.client.post('/auth/login/', {'email': '', 'password': '12341234'})
        assert_error_response(response, ErrorMessage.Type.INCORRECT_DATA)

    def test_4_login_empty_email_2(self):
        response = self.client.post('/auth/login/', {'password': '12341234'})
        assert_error_response(response, ErrorMessage.Type.INCORRECT_DATA)

    def test_5_login_empty_password(self):
        response = self.client.post('/auth/login/', {'email': 'test@eui.upm.es', 'password': ''})
        assert_error_response(response, ErrorMessage.Type.INCORRECT_DATA)

    def test_6_login_empty_password_2(self):
        response = self.client.post('/auth/login/', {'email': 'test@eui.upm.es'})
        assert_error_response(response, ErrorMessage.Type.INCORRECT_DATA)
