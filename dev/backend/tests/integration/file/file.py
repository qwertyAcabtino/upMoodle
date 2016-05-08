from rest.models import File
from rest.models.message.message import MessageType
from tests.integration.system import AuthenticationTestBase
from tests.utils import load_fixture, assert_ok_response


class FileTestCase(AuthenticationTestBase):
    def setUp(self):
        super(FileTestCase, self).setUp()
        load_fixture("provision-data")
        self.createUser()

    def _upload_file(self):
        with open('data/tests/default_update_avatar_pic.jpeg') as fp:
            self.login()
            response = self.file_client.post('/file/', data={
                'subject_id': 4,
                'uploader_id': 1,
                'name': 'Filename',
                'text': 'Description',
                'file': fp
            })
            assert_ok_response(response, MessageType.FILE_UPLOADED)
            return File.objects.get(pk=1)

    def test_new_file(self):
        self._upload_file()

    def test_update_file(self):
        test_file = self._upload_file()
        response = self.file_client.put('/file/' + test_file.hash,
                                        content_type='application/json',
                                        data={
                                            'name': 'NewFilename',
                                            'text': 'New Description',
                                        })
        assert_ok_response(response, MessageType.FILE_UPDATED)

    def test_delete_file(self):
        test_file = self._upload_file()
        response = self.file_client.delete('/file/' + test_file.hash)
        assert_ok_response(response, MessageType.FILE_REMOVED)

    def test_get_file(self):
        test_file = self._upload_file()
        response = self.file_client.delete('/file/' + test_file.hash)
        self.assertEqual(response.status_code, 200)
