from importlib import import_module

from django.test import TestCase, Client

from backend import settings
from backend.settings import SESSION_COOKIE_NAME
from upmoodle.models import User, NoteBoard
from tests.utils import JSONClient


class CookiesTestCase(TestCase):

    DEFAULT_TOKEN = 'DEFAULT_TOKEN'

    def setUp(self):
        self.client = JSONClient()
        self.file_client = Client()

        engine = import_module(settings.SESSION_ENGINE)
        session = engine.SessionStore()
        session[SESSION_COOKIE_NAME] = self.DEFAULT_TOKEN
        session.save()
        cookies = self.client.cookies
        cookies[SESSION_COOKIE_NAME] = self.DEFAULT_TOKEN
        self.file_client.cookies[SESSION_COOKIE_NAME] = self.DEFAULT_TOKEN


class AuthenticationTestBase(CookiesTestCase):

    DEFAULT_USER_NAME = 'Test user'
    DEFAULT_USER_NICK = 'Testuser'
    DEFAULT_USER_EMAIL = 'test@eui.upm.es'
    DEFAULT_USER_PASS = '12341234'

    DEFAULT_NOTE_TEXT = 'Bla bla'
    DEFAULT_NOTE_TOPIC = 'Topic'
    DEFAULT_NOTE_AUTHOR_ID = 1
    DEFAULT_NOTE_LEVEL_ID = 1

    def setUp(self):
        super(AuthenticationTestBase, self).setUp()

    def login(self):
        self.restoreUser()
        user = User.objects.get(id=1)
        user.sessionToken = self.DEFAULT_TOKEN
        user.save()

    def restorePassword(self):
        user = User.objects.get(id=1)
        user.password = self.DEFAULT_USER_PASS
        user.save()

    def logout(self):
        self.restoreUser()
        user = User.objects.get(id=1)
        user.sessionToken = ''
        user.save()

    def restoreUser(self):
        user = User.objects.get(id=1)
        user.name = self.DEFAULT_USER_NAME
        user.nick = self.DEFAULT_USER_NICK
        user.email = self.DEFAULT_USER_EMAIL
        user.password = self.DEFAULT_USER_PASS
        user.sessionToken = self.DEFAULT_TOKEN
        user.banned = False
        user.confirmedEmail = True
        user.save()

    def createUser(self):
        user = User()
        user.name = self.DEFAULT_USER_NAME
        user.nick = self.DEFAULT_USER_NICK
        user.email = self.DEFAULT_USER_EMAIL
        user.password = self.DEFAULT_USER_PASS
        user.sessionToken = self.DEFAULT_TOKEN
        user.banned = False
        user.confirmedEmail = True
        user.save()

    def addDefaultNote(self):
        note = NoteBoard()
        note.text = self.DEFAULT_NOTE_TEXT
        note.topic = self.DEFAULT_NOTE_TOPIC
        note.author_id = self.DEFAULT_NOTE_AUTHOR_ID
        note.level_id = self.DEFAULT_NOTE_LEVEL_ID
        note.save()
