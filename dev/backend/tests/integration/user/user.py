import json

from rest.MESSAGES_ID import *
from rest.controllers.controllers import get_random_email
from rest.models import User, Message, ErrorMessage, Rol

from tests.integration.system import AuthenticationTestBase
from tests.utils import load_fixture


class UserTestCase(AuthenticationTestBase):

    def setUp(self):
        super(UserTestCase, self).setUp()
        load_fixture("provision-data")
        self.createUser()

    def test_1_basic_getUser(self):
        self.login()
        pk = '1'
        response = self.client.get('/user/' + pk + '/')
        self.assertEqual(response.status_code, 200)

    def test_2_getUser_not_signed_in(self):
        self.logout()
        pk = '1'
        response = self.client.get('/user/' + pk + '/')
        self.assertEqual(response.status_code, 401)
        decoded = json.loads(response.content)
        self.assertEqual(ErrorMessage.objects.get(pk=NOT_SIGNED_IN).error, decoded['error'])

    def test_3_getUser_id_overflow(self):
        self.login()
        pk = '191289347901273481236498712634971234123481263984'
        response = self.client.get('/user/' + pk + '/')
        self.assertEqual(response.status_code, 400)
        decoded = json.loads(response.content)
        self.assertEqual(ErrorMessage.objects.get(pk=INCORRECT_DATA).error, decoded['error'])

    def test_4_basic_usersRol(self):
        self.login()
        rol = Rol.objects.get(name='Alumno')
        response = self.client.get('/users/rol/' + str(rol.id) + '/')
        self.assertEqual(response.status_code, 200)

    def test_5_usersRol_not_signedIn(self):
        self.logout()
        rol = Rol.objects.get(name='Alumno')
        response = self.client.get('/users/rol/' + str(rol.id) + '/')
        self.assertEqual(response.status_code, 401)
        decoded = json.loads(response.content)
        self.assertEqual(ErrorMessage.objects.get(pk=NOT_SIGNED_IN).error, decoded['error'])

    def test_6_userRol_id_overflow(self):
        self.login()
        rol = '191289347901273481236498712634971234123481263984'
        response = self.client.get('/users/rol/' + rol + '/')
        self.assertEqual(response.status_code, 400)
        decoded = json.loads(response.content)
        self.assertEqual(ErrorMessage.objects.get(pk=INCORRECT_DATA).error, decoded['error'])

    def test_7_userRemove_basic(self):
        self.login()
        response = self.client.delete('/user/')
        self.assertEqual(response.status_code, 200)
        user = User.objects.get(id=1)
        self.assertEqual(user.nick, 'RemovedUser ' + str(user.id))
        decoded = json.loads(response.content)
        self.assertEqual(Message.objects.get(pk=USER_REMOVED).message, decoded['message'])

    def test_8_userRemove_not_signedIn(self):
        self.logout()
        response = self.client.delete('/user/')
        self.assertEqual(response.status_code, 401)
        decoded = json.loads(response.content)
        self.assertEqual(ErrorMessage.objects.get(pk=NOT_SIGNED_IN).error, decoded['error'])

    def test_9_userUpdate_basic(self):
        self.login()
        newEmail = get_random_email()
        response = self.client.post('/user/', {'email': newEmail})
        self.assertEqual(response.status_code, 200)
        userUpdated = User.objects.get(id=1)
        self.assertEqual(userUpdated.email, newEmail)

    def test_10_userUpdate_change_forbidden_field(self):
        self.login()
        sessionToken = 'kaasdfbqwbiqwebibiweibef'
        response = self.client.post('/user/', {'sessionToken': sessionToken})
        self.assertEqual(response.status_code, 200)
        userUpdated = User.objects.get(id=1)
        self.assertNotEqual(userUpdated.sessionToken, sessionToken)

    def test_11_userUpdate_change_password(self):
        self.login()
        newPassword = 'qwerqwer'
        response = self.client.post('/user/', {'oldPassword': self.DEFAULT_USER_PASS, 'password': newPassword})
        self.assertEqual(response.status_code, 200)
        userUpdated = User.objects.get(id=1)
        self.assertEqual(userUpdated.password, newPassword)

    def test_12_userUpdate_change_password_bad(self):
        self.login()
        newPassword = 'qwerqwer'
        response = self.client.post('/user/', {'oldPassword': newPassword, 'password': newPassword})
        self.assertEqual(response.status_code, 400)
        decoded = json.loads(response.content)
        self.assertEqual(ErrorMessage.objects.get(pk=INCORRECT_DATA).error, decoded['error'])

    def test_13_userUpdate_basic_several(self):
        self.login()
        newEmail = 'email@upm.es'
        newName = 'Victor Perez rey'
        newNick = 'newNick'
        response = self.client.post('/user/', {'email': newEmail, 'name': newName, 'nick': newNick})
        self.assertEqual(response.status_code, 200)
        userUpdated = User.objects.get(id=1)
        self.assertEqual(userUpdated.name, newName)
        self.assertEqual(userUpdated.email, newEmail)
        self.assertEqual(userUpdated.nick, newNick)
