from django.utils.importlib import import_module
import json
from django.test import Client
from django.utils import unittest
from backend import settings
from rest.ERROR_MESSAGE_ID import PASSWORD_LENGTH, NICK_LENGTH, ALREADY_CONFIRMED, INVALID_TOKEN
from rest.models import Rol, LevelType, ErrorMessage, User

"""
unittest and not the django one for having persistency all along the *TestCase's
"""


class A_ErrorMessageTestCase(unittest.TestCase):
    def test_errormessages_exists_in_db(self):
        ErrorMessage.objects.create(error="Request cannot be performed")
        ErrorMessage.objects.create(error="Incorrect data")
        ErrorMessage.objects.create(error="Cookies disabled")
        ErrorMessage.objects.create(error="Already confirmed")
        ErrorMessage.objects.create(error="Invalid token")
        ErrorMessage.objects.create(error="User already in use")
        ErrorMessage.objects.create(error="Unauthorized")
        ErrorMessage.objects.create(error="Incorrect file data")
        ErrorMessage.objects.create(error="Password's length has to be between 8 and 100")
        ErrorMessage.objects.create(error="Nickname's length has to be between 4 and 20")
        ErrorMessage.objects.create(error="Email field cannot be empty")
        self.assertEqual(len(ErrorMessage.objects.all()), 11)


class B_RolTestCase(unittest.TestCase):
    def setUp(self):
        Rol.objects.create(name="g0d")
        Rol.objects.create(name="Alumno")
        Rol.objects.create(name="Profesor")
        Rol.objects.create(name="Coordinador de asignatura")
        Rol.objects.create(name="Delegado de curso")
        Rol.objects.create(name="Adminstrador")

    def test_roles_exits_in_db(self):
        self.assertEqual(len(Rol.objects.all()), 6)


class C_LevelTestCase(unittest.TestCase):
    def setUp(self):
        LevelType.objects.create(name="carrer")
        LevelType.objects.create(name="course")
        LevelType.objects.create(name="subject")

    def test_levels_exits_in_db(self):
        self.assertEqual(len(LevelType.objects.all()), 3)


class D_SignUpTestCase(unittest.TestCase):

    def setUp(self):
        self.client = Client()
        engine = import_module(settings.SESSION_ENGINE)
        session = self.client.session
        session = engine.SessionStore()
        session['cruasanPlancha'] = '.eJxVjEEOwiAQRe8ya0MgpKV06d4zEIaZ2oqBBGi6MN5dTLrQ7fvv_Rc4v7fV7ZWLW31dYQa0rKWeFoNGB2UJB5r0oEhKo3gZ0dpx0tYvcIHGtYWc48a9O3KJTJ3-XG4Es_oj6EPk1DHQw6d7FiGnVjYUX0WcaxW3TPy8nu77A9mHOJM:1Xpov5:Bnfuxp-BIVKSwSsUv7msEffLK70'
        session.save()
        cookies = self.client.cookies
        cookies['cruasanPlancha'] = '.eJxVjEEOwiAQRe8ya0MgpKV06d4zEIaZ2oqBBGi6MN5dTLrQ7fvv_Rc4v7fV7ZWLW31dYQa0rKWeFoNGB2UJB5r0oEhKo3gZ0dpx0tYvcIHGtYWc48a9O3KJTJ3-XG4Es_oj6EPk1DHQw6d7FiGnVjYUX0WcaxW3TPy8nu77A9mHOJM:1Xpov5:Bnfuxp-BIVKSwSsUv7msEffLK70'

    def test_basic_signup(self):
        response = self.client.post('/signup/', {'email': 'viperey@test.com', 'password': 'qwerqwere', 'nick': 'vipvip'})
        decoded = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(decoded['userId'])
        self.assertEqual(decoded['userId'], 1)
        self.assertEqual(len(User.objects.all()), 1)

    def test_duplicate_email(self):
        response = self.client.post('/signup/', {'email': 'viperey@test.com', 'password': 'qqwerwerqwere', 'nick': 'vqweripvip'})
        self.assertEqual(response.status_code, 400)
        decoded = json.loads(response.content)
        self.assertIsNotNone(decoded['error'])
        self.assertEqual(len(User.objects.all()), 1)

    def test_duplicate_nick(self):
        response = self.client.post('/signup/', {'email': 'viperey@test2.com', 'password': 'qwerqwere', 'nick': 'vipvip'})
        self.assertEqual(response.status_code, 400)
        decoded = json.loads(response.content)
        self.assertIsNotNone(decoded['error'])
        self.assertEqual(len(User.objects.all()), 1)

    def test_password_length(self):
        response = self.client.post('/signup/', {'email': 'viperey@test2.com', 'password': 'qwer', 'nick': 'vipvip'})
        self.assertEqual(response.status_code, 400)
        decoded = json.loads(response.content)
        self.assertIsNotNone(decoded['error'])
        self.assertEqual(len(User.objects.all()), 1)
        self.assertEqual(ErrorMessage.objects.get(pk=PASSWORD_LENGTH).error, decoded['error'])

    def test_password_length_2(self):
        response = self.client.post('/signup/', {'email': 'viperey@test2.com',
                                       'password': 'qwerwqwerqwqwerqwqwerqwqwerqwqwerqwqwerqwqwerqwqwerqwqwerqwqwerqwqwerqwqwerqwqwerqwqwerqwqwerqwqwqwer',
                                       'nick': 'vipvip'})
        self.assertEqual(response.status_code, 400)
        decoded = json.loads(response.content)
        self.assertIsNotNone(decoded['error'])
        self.assertEqual(len(User.objects.all()), 1)
        self.assertEqual(ErrorMessage.objects.get(pk=PASSWORD_LENGTH).error, decoded['error'])
        print response.content

    def test_nick_length(self):
        response = self.client.post('/signup/', {'email': 'viperey@test2.com', 'password': 'qwerqwerqwer', 'nick': 'qwe'})
        self.assertEqual(response.status_code, 400)
        decoded = json.loads(response.content)
        self.assertIsNotNone(decoded['error'])
        self.assertEqual(len(User.objects.all()), 1)
        self.assertEqual(ErrorMessage.objects.get(pk=NICK_LENGTH).error, decoded['error'])

    def test_nick_length_2(self):
        response = self.client.post('/signup/', {'email': 'viperey@test2.com', 'password': 'qwerqwerqwer',
                                       'nick': 'qweqweqweqweqweqweqweqwe'})
        self.assertEqual(response.status_code, 400)
        decoded = json.loads(response.content)
        self.assertIsNotNone(decoded['error'])
        self.assertEqual(len(User.objects.all()), 1)
        self.assertEqual(ErrorMessage.objects.get(pk=NICK_LENGTH).error, decoded['error'])

    def test_none_field_email(self):
        response = self.client.post('/signup/', {'email': '', 'password': 'qwerqwerqwer', 'nick': 'qweqwerqw'})
        self.assertEqual(response.status_code, 400)

    def test_none_field_email_2(self):
        response = self.client.post('/signup/', {'password': 'qwerqwerqwer', 'nick': 'qweqwerqw'})
        self.assertEqual(response.status_code, 400)

    def test_none_field_password(self):
        response = self.client.post('/signup/', {'email': 'viperey@test2.com', 'password': '', 'nick': 'qweqweqwer'})
        self.assertEqual(response.status_code, 400)

    def test_none_field_password_2(self):
        response = self.client.post('/signup/', {'email': 'viperey@test2.com', 'nick': 'qweqweqwer'})
        self.assertEqual(response.status_code, 400)

    def test_none_field_nick(self):
        response = self.client.post('/signup/', {'email': 'viperey@test2.com', 'password': 'qwerqwerqwer', 'nick': ''})
        self.assertEqual(response.status_code, 400)

    def test_none_field_nick_2(self):
        response = self.client.post('/signup/', {'email': 'viperey@test2.com', 'password': 'qwerqwerqwer'})
        self.assertEqual(response.status_code, 400)

    def test_none_field_2(self):
        response = self.client.post('/signup/', {'email': 'viperey@test2.com'})
        self.assertEqual(response.status_code, 400)

    def test_none_field_3(self):
        response = self.client.post('/signup/', {})
        self.assertEqual(response.status_code, 400)


class E_ConfirmEmailTestCase(unittest.TestCase):

    def setUp(self):
        self.client = Client()

    def test_1_basic_confirm(self):
        user = User.objects.get(id=1)
        response = self.client.get('/confirm_email/' + user.sessionToken + '/')
        self.assertEqual(response.status_code, 200)
        user = User.objects.get(id=1)
        self.assertFalse(user.banned)

    def test_2_already_confirmed(self):
        user = User.objects.get(id=1)
        response = self.client.get('/confirm_email/' + user.sessionToken + '/')
        self.assertEqual(response.status_code, 400)
        decoded = json.loads(response.content)
        self.assertEqual(ErrorMessage.objects.get(pk=ALREADY_CONFIRMED).error, decoded['error'])

    def test_3_invalid_token(self):
        user = User.objects.get(id=1)
        response = self.client.get('/confirm_email/randomdata/')
        self.assertEqual(response.status_code, 400)
        decoded = json.loads(response.content)
        self.assertEqual(ErrorMessage.objects.get(pk=INVALID_TOKEN).error, decoded['error'])

    def test_4_long_token(self):
        user = User.objects.get(id=1)
        response = self.client.get('/confirm_email/.eJxVjEEOwiAQRe8ya0MgpKV06d4zEIaZ2oqBBGi6MN5dTLrQ7fvv_Rc4v7fV7ZWLW31dYQa0rKWeFoNGB2UJB5r0oEhKo3gZ0dpx0tYvcIHGtYWc48a9O3KJTJ3-XG4Es_oj6EPk1DHQw6d7FiGnVjYUX0WcaxW3TPy8nu77A9mHOJM:1Xpov5:Bnfuxp-BIVKSwSsUv7msEffLK70adfsalsldflkasdjflaksjdflkasdjfkasdasdfhasdfasjdfijaosdifjaosidff/')
        self.assertEqual(response.status_code, 400)
        decoded = json.loads(response.content)
        self.assertEqual(ErrorMessage.objects.get(pk=INVALID_TOKEN).error, decoded['error'])
