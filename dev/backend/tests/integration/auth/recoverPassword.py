from rest.models import User
from rest.models.message.errorMessage import ErrorMessage
from rest.models.message.message import MessageType
from tests.integration.system import AuthenticationTestBase
from tests.utils import load_fixture, assert_error_response, assert_ok_response


class RecoverPasswordTestCase(AuthenticationTestBase):

    def setUp(self):
        super(RecoverPasswordTestCase, self).setUp()
        load_fixture("provision-data")
        self.createUser()

    def test_1_basic_recover(self):
        email = 'test@eui.upm.es'
        user = User.objects.get(email=email)
        passOld = user.password
        response = self.client.post('/auth/recover_password/', {'email': email})
        self.assertEqual(response.status_code, 200)
        user_new = User.objects.get(email=email)
        pass_new = user_new.password
        self.assertNotEqual(pass_new, passOld)
        assert_ok_response(response, MessageType.RECOVER_PASS_EMAIL)

    def test_2_unexisting_email(self):
        email = 'notExisting@test.com'
        response = self.client.post('/auth/recover_password/', {'email': email})
        assert_error_response(response, ErrorMessage.Type.INCORRECT_DATA)

    def test_3_empty_email(self):
        email = ''
        response = self.client.post('/auth/recover_password/', {'email': email})
        assert_error_response(response, ErrorMessage.Type.INCORRECT_DATA)

    def test_4_banned_user(self):
        email = 'test@eui.upm.es'
        user = User.objects.get(email=email)
        user.banned = True
        user.save()
        response = self.client.post('/auth/recover_password/', {'email': email})
        assert_error_response(response, ErrorMessage.Type.UNAUTHORIZED)
        user.banned = False
        user.save()

    def test_5_unconfirmed_user(self):
        email = 'test@eui.upm.es'
        user = User.objects.get(email=email)
        user.confirmedEmail = False
        user.save()
        response = self.client.post('/auth/recover_password/', {'email': email})
        assert_error_response(response, ErrorMessage.Type.UNCONFIRMED_EMAIL)
        user.confirmedEmail = True
        user.save()
