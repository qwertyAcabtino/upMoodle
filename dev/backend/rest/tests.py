from django.utils.importlib import import_module
import json
from django.test import Client, RequestFactory, TestCase
from django.utils import unittest
from backend import settings
from backend.settings import SESSION_COOKIE_NAME, SESSION_COOKIE_NAME_BIS
from rest.MESSAGES_ID import PASSWORD_LENGTH, NICK_LENGTH, ALREADY_CONFIRMED, INVALID_TOKEN, UNCONFIRMED_EMAIL, \
    INCORRECT_DATA, DISABLED_COOKIES, RECOVER_PASS_EMAIL, UNAUTHORIZED, NOT_SIGNED_IN, USER_REMOVED, EMAIL_INVALID
from rest.controllers.controllers import get_random_string, get_random_email
from rest.models import Rol, LevelType, ErrorMessage, User, Message, NoteBoard, Level
from rest.router import login

"""
unittest and not the django one for having persistency all along the *TestCase's
"""

defPassword = '12341234'
sessionCookie = '.eJxVjEEOwiAQRe8ya0MgpKV06d4zEIaZ2oqBBGi6MN5dTLrQ7fvv_Rc4v7fV7ZWLW31dYQa0rKWeFoNGB2UJB5r0oEhKo3gZ0dpx0tYvcIHGtYWc48a9O3KJTJ3-XG4Es_oj6EPk1DHQw6d7FiGnVjYUX0WcaxW3TPy8nu77A9mHOJM:1Xpov5:Bnfuxp-BIVKSwSsUv7msEffLK70'
defUser = User()
defUser.name = 'Test user'
defUser.nick = 'Testuser'
defUser.email = 'test@eui.upm.es'
defUser.password = defPassword
defUser.sessionToken = sessionCookie

defNote = NoteBoard()
defNote.text = 'Bla bla'
defNote.topic = 'Topic'
defNote.author_id = 1

class CookiesEnabled(unittest.TestCase):
    def setUp(self):
        self.client = Client()
        engine = import_module(settings.SESSION_ENGINE)
        session = self.client.session
        session = engine.SessionStore()
        session[SESSION_COOKIE_NAME_BIS] = sessionCookie
        session[SESSION_COOKIE_NAME] = sessionCookie
        session.save()
        cookies = self.client.cookies
        cookies[SESSION_COOKIE_NAME_BIS] = sessionCookie
        cookies[SESSION_COOKIE_NAME] = sessionCookie


class SignedTestCase(CookiesEnabled):
    def setUp(self):
        super(SignedTestCase, self).setUp()
        self.restorePassword()

    def login(self):
        self.restoreUser()
        user = User.objects.get(id=1)
        user.sessionToken = sessionCookie
        user.save()

    def restorePassword(self):
        user = User.objects.get(id=1)
        user.password = defPassword
        user.save()

    def logout(self):
        self.restoreUser()
        user = User.objects.get(id=1)
        user.sessionToken = ''
        user.save()

    def restoreUser(self):
        user = User.objects.get(id=1)
        user.name = defUser.name
        user.nick = defUser.nick
        user.email = defUser.email
        user.password = defUser.password
        user.sessionToken = sessionCookie
        user.banned = False
        user.confirmedEmail = True
        user.save()

    def addDefaultNote(self):
        note = defNote
        note.author_id = 1
        note.level_id = 1
        note.save()


class A1_ErrorMessageTestCase(unittest.TestCase):
    def test_errormessages_exists_in_db(self):
        ErrorMessage.objects.create(error="Request cannot be performed")
        ErrorMessage.objects.create(error="Incorrect data")
        ErrorMessage.objects.create(error="Cookies are disabled")
        ErrorMessage.objects.create(error="Already confirmed")
        ErrorMessage.objects.create(error="Invalid token")
        ErrorMessage.objects.create(error="User already in use")
        ErrorMessage.objects.create(error="Unauthorized")
        ErrorMessage.objects.create(error="Incorrect file data")
        ErrorMessage.objects.create(error="Password's length has to be between 8 and 100")
        ErrorMessage.objects.create(error="Nickname's length has to be between 4 and 20")
        ErrorMessage.objects.create(error="Email field cannot be empty")
        ErrorMessage.objects.create(error="Please, check your inbox and confirm your email.")
        ErrorMessage.objects.create(error="Please, sign in first.")
        self.assertEqual(len(ErrorMessage.objects.all()), 13)


class A2_MessageTestCase(unittest.TestCase):
    def setUp(self):
        Message.objects.create(message="Successfully signed in")
        Message.objects.create(message="Email is now confirmed")
        Message.objects.create(message="A new password has been sent to your email adress. Check your inbox")
        Message.objects.create(message="Your user account has been removed.")
        Message.objects.create(message="Your profile has been updated")
        Message.objects.create(message="Note updated")

    def test_messages_exists_in_db(self):
        self.assertEqual(len(Message.objects.all()), 6)


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


class C1_LevelTypeTestCase(unittest.TestCase):
    def setUp(self):
        LevelType.objects.create(name="carrer")
        LevelType.objects.create(name="course")
        LevelType.objects.create(name="subject")

    def test_leveltypes_exits_in_db(self):
        self.assertEqual(len(LevelType.objects.all()), 3)


class C2_LevelTypeTestCase(unittest.TestCase):

    def setUp(self):
        level = Level()
        level.name = "Level 1"
        level.visible = True
        level.type = LevelType.objects.get(id=1)
        level.save()

    def test_levels_exists_in_db(self):
        self.assertEqual(len(Level.objects.all()), 1)

class D_SignUpTestCase(CookiesEnabled):

    def test_basic_signup(self):
        response = self.client.post('/signup/',
                                    {'email': 'test@eui.upm.es', 'password': '12341234', 'nick': 'vipvip'})
        decoded = json.loads(response.content)
        defaultUser = User.objects.get(id=1)
        defaultUser.save()
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(decoded['userId'])
        self.assertEqual(decoded['userId'], 1)
        self.assertEqual(len(User.objects.all()), 1)

    def test_duplicate_email(self):
        response = self.client.post('/signup/',
                                    {'email': 'test112312@eui.upm.es', 'password': 'qqwerwerqwere', 'nick': 'vqweripasdfvip'})
        self.assertEqual(response.status_code, 400)
        decoded = json.loads(response.content)
        self.assertIsNotNone(decoded['error'])
        self.assertEqual(len(User.objects.all()), 1)

    def test_1_invalid_email(self):
        response = self.client.post('/signup/',
                                    {'email': 'test112@google.com', 'password': 'qqwerwerqwere', 'nick': 'vqwsdfsdferipvip'})
        self.assertEqual(response.status_code, 400)
        decoded = json.loads(response.content)
        self.assertIsNotNone(decoded['error'])
        self.assertEqual(len(User.objects.all()), 0)
        self.assertEqual(ErrorMessage.objects.get(pk=EMAIL_INVALID).error, decoded['error'])

    def test_duplicate_nick(self):
        response = self.client.post('/signup/',
                                    {'email': 'viperey@eui.upm.es', 'password': '12341234', 'nick': 'vipvip'})
        self.assertEqual(response.status_code, 400)
        decoded = json.loads(response.content)
        self.assertIsNotNone(decoded['error'])
        self.assertEqual(len(User.objects.all()), 1)

    def test_password_length(self):
        response = self.client.post('/signup/', {'email': 'viperey@eui.upm.es', 'password': 'qwer', 'nick': 'vipvip'})
        self.assertEqual(response.status_code, 400)
        decoded = json.loads(response.content)
        self.assertIsNotNone(decoded['error'])
        self.assertEqual(len(User.objects.all()), 1)
        self.assertEqual(ErrorMessage.objects.get(pk=PASSWORD_LENGTH).error, decoded['error'])

    def test_password_length_2(self):
        response = self.client.post('/signup/', {'email': 'viperey@eui.upm.es',
                                                 'password': 'qwerwqwerqwqwerqwqwerqwqwerqwqwerqwqwerqwqwerqwqwerqwqwerqwqwerqwqwerqwqwerqwqwerqwqwerqwqwerqwqwqwer',
                                                 'nick': 'vipvip'})
        self.assertEqual(response.status_code, 400)
        decoded = json.loads(response.content)
        self.assertIsNotNone(decoded['error'])
        self.assertEqual(len(User.objects.all()), 1)
        self.assertEqual(ErrorMessage.objects.get(pk=PASSWORD_LENGTH).error, decoded['error'])
        print response.content

    def test_nick_length(self):
        response = self.client.post('/signup/',
                                    {'email': 'viperey@eui.upm.es', 'password': 'qwerqwerqwer', 'nick': 'qwe'})
        self.assertEqual(response.status_code, 400)
        decoded = json.loads(response.content)
        self.assertIsNotNone(decoded['error'])
        self.assertEqual(len(User.objects.all()), 1)
        self.assertEqual(ErrorMessage.objects.get(pk=NICK_LENGTH).error, decoded['error'])

    def test_nick_length_2(self):
        response = self.client.post('/signup/', {'email': 'viperey@eui.upm.es', 'password': 'qwerqwerqwer',
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


class E_ConfirmEmailTestCase(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_1_basic_confirm(self):
        user = User.objects.get(id=1)
        response = self.client.get('/confirm_email/' + user.sessionToken + '/')
        self.assertEqual(response.status_code, 200)
        user = User.objects.get(id=1)
        self.assertTrue(user.confirmedEmail)

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
        response = self.client.get(
            '/confirm_email/.eJxVjEEOwiAQRe8ya0MgpKV06d4zEIaZ2oqBBGi6MN5dTLrQ7fvv_Rc4v7fV7ZWLW31dYQa0rKWeFoNGB2UJB5r0oEhKo3gZ0dpx0tYvcIHGtYWc48a9O3KJTJ3-XG4Es_oj6EPk1DHQw6d7FiGnVjYUX0WcaxW3TPy8nu77A9mHOJM:1Xpov5:Bnfuxp-BIVKSwSsUv7msEffLK70adfsalsldflkasdjflaksjdflkasdjfkasdasdfhasdfasjdfijaosdifjaosidff/')
        self.assertEqual(response.status_code, 400)
        decoded = json.loads(response.content)
        self.assertEqual(ErrorMessage.objects.get(pk=INVALID_TOKEN).error, decoded['error'])


class F_LoginTestCase(CookiesEnabled):

    def test_1_basic_login(self):
        response = self.client.post('/login/', {'email': 'test@eui.upm.es', 'password': '12341234'})
        self.assertEqual(response.status_code, 200)
        user = User.objects.get(email='test@eui.upm.es')
        self.assertTrue(user.confirmedEmail)

    def test_2_login_unconfirmed_email(self):
        user = User.objects.get(email='test@eui.upm.es')
        user.confirmedEmail = False
        user.save()
        response = self.client.post('/login/', {'email': 'test@eui.upm.es', 'password': '12341234'})
        self.assertEqual(response.status_code, 400)
        decoded = json.loads(response.content)
        self.assertEqual(ErrorMessage.objects.get(pk=UNCONFIRMED_EMAIL).error, decoded['error'])
        user = User.objects.get(email='test@eui.upm.es')
        user.confirmedEmail = True
        user.save()

    def test_3_login_empty_email(self):
        response = self.client.post('/login/', {'email': '', 'password': '12341234'})
        self.assertEqual(response.status_code, 400)
        decoded = json.loads(response.content)
        self.assertEqual(ErrorMessage.objects.get(pk=INCORRECT_DATA).error, decoded['error'])

    def test_4_login_empty_email_2(self):
        response = self.client.post('/login/', {'password': '12341234'})
        self.assertEqual(response.status_code, 400)
        decoded = json.loads(response.content)
        self.assertEqual(ErrorMessage.objects.get(pk=INCORRECT_DATA).error, decoded['error'])

    def test_5_login_empty_password(self):
        response = self.client.post('/login/', {'email': 'test@eui.upm.es', 'password': ''})
        self.assertEqual(response.status_code, 400)
        decoded = json.loads(response.content)
        self.assertEqual(ErrorMessage.objects.get(pk=INCORRECT_DATA).error, decoded['error'])

    def test_6_login_empty_password_2(self):
        response = self.client.post('/login/', {'email': 'test@eui.upm.es'})
        self.assertEqual(response.status_code, 400)
        decoded = json.loads(response.content)
        self.assertEqual(ErrorMessage.objects.get(pk=INCORRECT_DATA).error, decoded['error'])

    # In this case, for testing the behaviour when having cookies disabled, the request has to be made in a special way.
    def test_7_login_disabled_cookies(self):
        request = RequestFactory().post('/login/', {'email': 'test@eui.upm.es', 'password': '12341234'})
        request.COOKIES[SESSION_COOKIE_NAME_BIS] = None
        request.session = self.client.session
        request.session.TEST_COOKIE_VALUE = None

        response = login(request)
        self.assertEqual(response.status_code, 400)
        decoded = json.loads(response.content)
        self.assertEqual(ErrorMessage.objects.get(pk=DISABLED_COOKIES).error, decoded['error'])

    def test_8_login_disabled_cookies_2(self):
        request = RequestFactory().post('/login/', {'email': 'test@eui.upm.es', 'password': '12341234'})
        request.session = self.client.session
        request.COOKIES[SESSION_COOKIE_NAME_BIS] = None

        response = login(request)
        self.assertEqual(response.status_code, 400)
        decoded = json.loads(response.content)
        self.assertEqual(ErrorMessage.objects.get(pk=DISABLED_COOKIES).error, decoded['error'])

    def test_8_login_disabled_cookies_3(self):
        request = RequestFactory().post('/login/', {'email': 'test@eui.upm.es', 'password': '12341234'})
        request.session = self.client.session
        request.COOKIES[SESSION_COOKIE_NAME_BIS] = ''

        response = login(request)
        self.assertEqual(response.status_code, 400)
        decoded = json.loads(response.content)
        self.assertEqual(ErrorMessage.objects.get(pk=DISABLED_COOKIES).error, decoded['error'])


class G_LogoutTestCase(SignedTestCase):
    def test_1_logout_basic(self):
        response = self.client.post('/logout/')
        self.assertEqual(response.status_code, 200)


class H_RecoverPasswordTestCase(unittest.TestCase):
    def setUp(self):
        self.client = Client()

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
        self.assertEqual(response.status_code, 400)
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


class I_userTestCase(SignedTestCase):
    def test_1_basic_getUser(self):
        self.login()
        pk = '1'
        response = self.client.get('/user/' + pk + '/')
        self.assertEqual(response.status_code, 200)

    def test_2_getUser_not_signed_in(self):
        self.logout()
        pk = '1'
        response = self.client.get('/user/' + pk + '/')
        self.assertEqual(response.status_code, 400)
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
        self.assertEqual(response.status_code, 400)
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
        self.assertEqual(response.status_code, 400)
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
        response = self.client.post('/user/', {'oldPassword': defPassword, 'password': newPassword})
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


class J_noteTestCase(SignedTestCase):
    def test_1_basic_note_get(self):
        self.login()
        self.addDefaultNote()
        pk = '1'
        response = self.client.get('/note/' + pk + '/')
        self.assertEqual(response.status_code, 200)
        decoded = json.loads(response.content)
        self.assertIsNotNone(decoded['id'])
        self.assertEqual(decoded['topic'], defNote.topic)

    def test_2_getNote_not_signed_in(self):
        self.logout()
        pk = '1'
        response = self.client.get('/note/' + pk + '/')
        self.assertEqual(response.status_code, 400)
        decoded = json.loads(response.content)
        self.assertEqual(ErrorMessage.objects.get(pk=NOT_SIGNED_IN).error, decoded['error'])

    def test_3_getNote_id_overflow(self):
        self.login()
        pk = '191289347901273481236498712634971234123481263984'
        response = self.client.get('/note/' + pk + '/')
        self.assertEqual(response.status_code, 400)
        decoded = json.loads(response.content)
        self.assertEqual(ErrorMessage.objects.get(pk=INCORRECT_DATA).error, decoded['error'])

    def test_4_postNote_basic(self):
        self.login()
        pk = 1
        topic = 'topic'
        response = self.client.post('/note/' + str(pk) + '/', {'topic': topic, 'text': 'text', 'level_id': 1})
        self.assertEqual(response.status_code, 200)
        note = NoteBoard.objects.get(id=1)
        self.assertEqual(topic, note.topic)

    def test_5_postNote_signedOut(self):
        self.logout()
        pk = 1
        topic = 'topic'
        response = self.client.post('/note/' + str(pk) + '/', {'topic': topic, 'text': 'text', 'level_id': 1})
        self.assertEqual(response.status_code, 400)

    def test_6_postNote_forbiddenFields(self):
        self.login()
        pk = 1
        topic = 'topic'
        response = self.client.post('/note/' + str(pk) + '/', {'topic': topic, 'text': 'text', 'author_id': 2})
        self.assertEqual(response.status_code, 200)
        note = NoteBoard.objects.get(id=1)
        self.assertEqual(note.author_id, User.objects.get(id=1).id)

    def test_7_postNote_emptyQuery(self):
        self.login()
        pk = 1
        response = self.client.post('/note/' + str(pk) + '/', {})
        self.assertEqual(response.status_code, 200)

    def test_8_postNote_length_overflows(self):
        self.login()
        pk = 1
        # Topic
        response = self.client.post('/note/' + str(pk) + '/', {'topic': sessionCookie, 'text': 'text', 'level_id': 1})
        decoded = json.loads(response.content)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(ErrorMessage.objects.get(pk=INCORRECT_DATA).error, decoded['error'])
        # Text
        response = self.client.post('/note/' + str(pk) + '/', {'topic': 'topic', 'text': get_random_string(2001), 'level_id': 1})
        decoded = json.loads(response.content)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(ErrorMessage.objects.get(pk=INCORRECT_DATA).error, decoded['error'])

