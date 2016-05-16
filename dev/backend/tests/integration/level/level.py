import json

from django.test import TestCase

from upmoodle.models import Level
from upmoodle.models.message.errorMessage import ErrorMessage
from tests import utils
from tests.integration.auth.system import AuthenticationTestBase
from tests.utils import load_fixture, assert_error_response


class LevelTestCase(TestCase):

    def setUp(self):
        load_fixture("provision-data")

    def test_level_exits_in_db(self):
        self.assertEqual(len(Level.objects.all()), 10)


class LevelNotesTestCase(AuthenticationTestBase):

    def setUp(self):
        super(LevelNotesTestCase, self).setUp()
        load_fixture("provision-data")
        self.createUser()

    def _create_random_note(self, level_id=0):
        topic = 'Create' + utils.get_random_string(10)
        response = self.client.post('/note/', {
            'topic': topic,
            'text': 'text',
            'level_id': level_id
        })
        self.assertEqual(response.status_code, 201)

    def test_get_notes(self):
        self._create_random_note(level_id=1)
        self._create_random_note(level_id=3)
        response = self.client.get('/level/1/notes?recursive=true')
        notes = json.loads(response.content)['data']
        assert len(notes) is 2

        response = self.client.get('/level/1/notes?recursive=false')
        notes = json.loads(response.content)['data']
        assert len(notes) is 1


class LevelFilesTestCase(AuthenticationTestBase):

    def setUp(self):
        super(LevelFilesTestCase, self).setUp()
        load_fixture("provision-data")
        self.createUser()

    def test_get_files_(self):
        file_uploaded = utils._upload_file(self, level_id=4)
        file_uploaded = utils._upload_file(self, level_id=4)
        response = self.client.get('/level/4/files')
        files = json.loads(response.content)['data']
        assert len(files) is 2

    def test_get_files_no_subject(self):
        file_uploaded = utils._upload_file(self, level_id=4)
        response = self.client.get('/level/1/files')
        assert_error_response(response, ErrorMessage.Type.INVALID_LEVEL)
