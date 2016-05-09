from rest.models import User
from rest.models.message.errorMessage import ErrorMessage
from rest.models.message.message import MessageType
from rest.services.utils.email import EmailService

from tests.integration.system import AuthenticationTestBase
from tests.utils import load_fixture, assert_error_response, assert_ok_response


class UserMeTestCase(AuthenticationTestBase):

    def setUp(self):
        super(UserMeTestCase, self).setUp()
        load_fixture("provision-data")
        self.createUser()

    def test_userRemove_basic(self):
        self.login()
        response = self.client.delete('/user/')
        self.assertEqual(response.status_code, 200)
        user = User.objects.get(id=1)
        self.assertEqual(user.nick, 'RemovedUser ' + str(user.id))
        assert_ok_response(response, MessageType.USER_REMOVED)

    def test_userRemove_not_signedIn(self):
        self.logout()
        response = self.client.delete('/user/')
        assert_error_response(response, ErrorMessage.Type.NOT_SIGNED_IN)

    def test_userUpdate_basic(self):
        self.login()
        new_email = EmailService.get_random_email()
        response = self.client.post('/user/', {'email': new_email})
        self.assertEqual(response.status_code, 200)
        updated_user = User.objects.get(id=1)
        self.assertEqual(updated_user.email, new_email)

    def test_userUpdate_change_forbidden_field(self):
        self.login()
        token = 'kaasdfbqwbiqwebibiweibef'
        response = self.client.post('/user/', {'sessionToken': token})
        self.assertEqual(response.status_code, 200)
        updated_user = User.objects.get(id=1)
        self.assertNotEqual(updated_user.sessionToken, token)

    def test_userUpdate_change_password(self):
        self.login()
        new_pass = 'qwerqwer'
        response = self.client.post('/user/', {'oldPassword': self.DEFAULT_USER_PASS, 'password': new_pass})
        self.assertEqual(response.status_code, 200)
        updated_user = User.objects.get(id=1)
        self.assertEqual(updated_user.password, new_pass)

    def test_userUpdate_change_password_bad(self):
        self.login()
        new_password = 'qwerqwer'
        response = self.client.post('/user/', {'oldPassword': new_password, 'password': new_password})
        assert_error_response(response, ErrorMessage.Type.INCORRECT_DATA)

    def test_userUpdate_basic_several(self):
        self.login()
        new_email = 'email@upm.es'
        new_name = 'Victor Perez rey'
        new_nick = 'newNick'
        response = self.client.post('/user/', {'email': new_email, 'name': new_name, 'nick': new_nick})
        self.assertEqual(response.status_code, 200)
        updated_user = User.objects.get(id=1)
        self.assertEqual(updated_user.name, new_name)
        self.assertEqual(updated_user.email, new_email)
        self.assertEqual(updated_user.nick, new_nick)

    def test_update_avatar(self):
        with open('data/tests/default_update_avatar_pic.jpeg') as fp:
            self.login()
            response = self.file_client.post('/user/avatar/', data={'avatar': fp})
            assert_ok_response(response, MessageType.USER_UPDATED)

    def test_update_avatar_bad_reference(self):
        with open('data/tests/default_update_avatar_pic.jpeg') as fp:
            self.login()
            response = self.file_client.post('/user/avatar/', data={'incorrect_field_name': fp})
            assert_error_response(response, ErrorMessage.Type.INCORRECT_DATA)
