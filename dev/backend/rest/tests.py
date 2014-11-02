import json
from django.test import Client
from django.test.simple import DjangoTestSuiteRunner
from django.utils import unittest
from rest.ERROR_MESSAGE_ID import PASSWORD_LENGTH, NICK_LENGTH
from rest.models import Rol, LevelType, ErrorMessage, User

"""
unittest and not the django one for having persistency all along the *TestCase's
"""
class ErrorMessageTestCase(unittest.TestCase):

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


class RolTestCase(unittest.TestCase):

    def setUp(self):
        Rol.objects.create(name="g0d")
        Rol.objects.create(name="Alumno")
        Rol.objects.create(name="Profesor")
        Rol.objects.create(name="Coordinador de asignatura")
        Rol.objects.create(name="Delegado de curso")
        Rol.objects.create(name="Adminstrador")

    def test_roles_exits_in_db(self):
        self.assertEqual(len(Rol.objects.all()), 6)


class LevelTestCase(unittest.TestCase):

    def setUp(self):
        LevelType.objects.create(name="carrer")
        LevelType.objects.create(name="course")
        LevelType.objects.create(name="subject")

    def test_levels_exits_in_db(self):
        self.assertEqual(len(LevelType.objects.all()), 3)


class SignUpTestCase(unittest.TestCase):


    def test_basic_signup(self):
        c = Client()
        response = c.post('/signup/', {'email': 'viperey@test.com', 'password': 'qwerqwere', 'nick': 'vipvip'})
        self.assertEqual(response.status_code, 200)
        decoded = json.loads(response.content)
        self.assertIsNotNone(decoded['userId'])
        self.assertEqual(decoded['userId'], 1)
        self.assertEqual(len(User.objects.all()), 1)

    def test_duplicate_email(self):
        c = Client()
        response = c.post('/signup/', {'email': 'viperey@test.com', 'password': 'qqwerwerqwere', 'nick': 'vqweripvip'})
        self.assertEqual(response.status_code, 400)
        decoded = json.loads(response.content)
        self.assertIsNotNone(decoded['error'])
        self.assertEqual(len(User.objects.all()), 1)

    def test_duplicate_nick(self):
        c = Client()
        response = c.post('/signup/', {'email': 'viperey@test2.com', 'password': 'qwerqwere', 'nick': 'vipvip'})
        self.assertEqual(response.status_code, 400)
        decoded = json.loads(response.content)
        self.assertIsNotNone(decoded['error'])
        self.assertEqual(len(User.objects.all()), 1)

    def test_password_length(self):
        c = Client()
        response = c.post('/signup/', {'email': 'viperey@test2.com', 'password': 'qwer', 'nick': 'vipvip'})
        self.assertEqual(response.status_code, 400)
        decoded = json.loads(response.content)
        self.assertIsNotNone(decoded['error'])
        self.assertEqual(len(User.objects.all()), 1)
        self.assertEqual(ErrorMessage.objects.get(pk=PASSWORD_LENGTH).error, decoded['error'])

    def test_password_length_2(self):
        c = Client()
        response = c.post('/signup/', {'email': 'viperey@test2.com', 'password': 'qwerwqwerqwqwerqwqwerqwqwerqwqwerqwqwerqwqwerqwqwerqwqwerqwqwerqwqwerqwqwerqwqwerqwqwerqwqwerqwqwqwer', 'nick': 'vipvip'})
        self.assertEqual(response.status_code, 400)
        decoded = json.loads(response.content)
        self.assertIsNotNone(decoded['error'])
        self.assertEqual(len(User.objects.all()), 1)
        self.assertEqual(ErrorMessage.objects.get(pk=PASSWORD_LENGTH).error, decoded['error'])
        print response.content

    def test_nick_length(self):
        c = Client()
        response = c.post('/signup/', {'email': 'viperey@test2.com', 'password': 'qwerqwerqwer', 'nick': 'qwe'})
        self.assertEqual(response.status_code, 400)
        decoded = json.loads(response.content)
        self.assertIsNotNone(decoded['error'])
        self.assertEqual(len(User.objects.all()), 1)
        self.assertEqual(ErrorMessage.objects.get(pk=NICK_LENGTH).error, decoded['error'])

    def test_nick_length_2(self):
        c = Client()
        response = c.post('/signup/', {'email': 'viperey@test2.com', 'password': 'qwerqwerqwer', 'nick': 'qweqweqweqweqweqweqweqwe'})
        self.assertEqual(response.status_code, 400)
        decoded = json.loads(response.content)
        self.assertIsNotNone(decoded['error'])
        self.assertEqual(len(User.objects.all()), 1)
        self.assertEqual(ErrorMessage.objects.get(pk=NICK_LENGTH).error, decoded['error'])

    def test_none_field_email(self):
        c = Client()
        response = c.post('/signup/', {'email': '', 'password': 'qwerqwerqwer', 'nick': 'qweqwerqw'})
        self.assertEqual(response.status_code, 400)

    def test_none_field_email_2(self):
        c = Client()
        response = c.post('/signup/', {'password': 'qwerqwerqwer', 'nick': 'qweqwerqw'})
        self.assertEqual(response.status_code, 400)

    def test_none_field_password(self):
        c = Client()
        response = c.post('/signup/', {'email': 'viperey@test2.com', 'password': '', 'nick': 'qweqweqwer'})
        self.assertEqual(response.status_code, 400)

    def test_none_field_password_2(self):
        c = Client()
        response = c.post('/signup/', {'email': 'viperey@test2.com', 'nick': 'qweqweqwer'})
        self.assertEqual(response.status_code, 400)

    def test_none_field_nick(self):
        c = Client()
        response = c.post('/signup/', {'email': 'viperey@test2.com', 'password': 'qwerqwerqwer', 'nick': ''})
        self.assertEqual(response.status_code, 400)

    def test_none_field_nick_2(self):
        c = Client()
        response = c.post('/signup/', {'email': 'viperey@test2.com', 'password': 'qwerqwerqwer'})
        self.assertEqual(response.status_code, 400)

    def test_none_field_2(self):
        c = Client()
        response = c.post('/signup/', {'email': 'viperey@test2.com'})
        self.assertEqual(response.status_code, 400)

    def test_none_field_3(self):
        c = Client()
        response = c.post('/signup/', {})
        self.assertEqual(response.status_code, 400)


