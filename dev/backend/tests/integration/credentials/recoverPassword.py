import json

from rest.MESSAGES_ID import *
from rest.models import User, Message, ErrorMessage
from tests.integration.system import AuthenticationTestBase
from tests.utils import load_fixture


class RecoverPasswordTestCase(AuthenticationTestBase):

    def setUp(self):
        super(RecoverPasswordTestCase, self).setUp()
        load_fixture("provision-data")
        self.createUser()

    def test_1_basic_recover(self):
        email = 'test@eui.upm.es'
        user = User.objects.get(email=email)
        passOld = user.password
        response = self.client.post('/recover_password/', {'email': email})
        self.assertEqual(response.status_code, 200)
        userNew = User.objects.get(email=email)
        passNew = userNew.password
        self.assertNotEqual(passNew, passOld)
        decoded = json.loads(response.content)
        self.assertEqual(Message.objects.get(pk=RECOVER_PASS_EMAIL).message, decoded['message'])

    def test_2_unexisting_email(self):
        email = 'notExisting@test.com'
        response = self.client.post('/recover_password/', {'email': email})
        self.assertEqual(response.status_code, 400)
        decoded = json.loads(response.content)
        self.assertEqual(ErrorMessage.objects.get(pk=INCORRECT_DATA).error, decoded['error'])

    def test_3_empty_email(self):
        email = ''
        response = self.client.post('/recover_password/', {'email': email})
        self.assertEqual(response.status_code, 400)
        decoded = json.loads(response.content)
        self.assertEqual(ErrorMessage.objects.get(pk=INCORRECT_DATA).error, decoded['error'])

    def test_4_banned_user(self):
        email = 'test@eui.upm.es'
        user = User.objects.get(email=email)
        user.banned = True
        user.save()
        response = self.client.post('/recover_password/', {'email': email})
        self.assertEqual(response.status_code, 401)
        decoded = json.loads(response.content)
        self.assertEqual(ErrorMessage.objects.get(pk=UNAUTHORIZED).error, decoded['error'])
        user.banned = False
        user.save()

    def test_5_unconfirmed_user(self):
        email = 'test@eui.upm.es'
        user = User.objects.get(email=email)
        user.confirmedEmail = False
        user.save()
        response = self.client.post('/recover_password/', {'email': email})
        self.assertEqual(response.status_code, 400)
        decoded = json.loads(response.content)
        self.assertEqual(ErrorMessage.objects.get(pk=UNCONFIRMED_EMAIL).error, decoded['error'])
        user.confirmedEmail = True
        user.save()
