import json

from upmoodle.models import User
from upmoodle.models.message.errorMessage import ErrorMessage
from upmoodle.models.message.okMessage import OkMessage

from tests.integration.auth.system import AuthenticationTestBase
from tests import utils


class UserMeTestCase(AuthenticationTestBase):

    def setUp(self):
        super(UserMeTestCase, self).setUp()
        utils.load_fixture("provision-data")
        self.createUser()

    def test_get_user(self):
        self.login()
        response = self.client.get('/user/')
        self.assertEqual(response.status_code, 200)
        decoded = json.loads(response.content)
        self.assertIsNotNone(decoded)

    def test_get_users(self):
        self.login()
        response = self.client.get('/user/')
        self.assertEqual(response.status_code, 200)
        decoded = json.loads(response.content)
        self.assertIsNotNone(decoded)

    def test_userRemove_basic(self):
        self.login()
        response = self.client.delete('/user/')
        self.assertEqual(response.status_code, 200)
        user = User.objects.get(id=1)
        self.assertEqual(user.nick, 'RemovedUser ' + str(user.id))
        utils.assert_ok_response(response, OkMessage.Type.USER_REMOVED)

    def test_userRemove_not_signedIn(self):
        self.logout()
        response = self.client.delete('/user/')
        utils.assert_error_response(response, ErrorMessage.Type.NOT_SIGNED_IN)

    def test_userUpdate_basic(self):
        self.login()
        new_email = utils.get_random_email()
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
        utils.assert_error_response(response, ErrorMessage.Type.INCORRECT_DATA)

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
            utils.assert_ok_response(response, OkMessage.Type.USER_UPDATED)

    def test_update_avatar_bad_reference(self):
        with open('data/tests/default_update_avatar_pic.jpeg') as fp:
            self.login()
            response = self.file_client.post('/user/avatar/', data={'incorrect_field_name': fp})
            utils.assert_error_response(response, ErrorMessage.Type.INCORRECT_DATA)
