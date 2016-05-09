from upmoodle.models.message.okMessage import OkMessage
from tests import utils
from tests.integration.auth.system import AuthenticationTestBase
from tests.utils import load_fixture, assert_ok_response


class FileTestCase(AuthenticationTestBase):
    def setUp(self):
        super(FileTestCase, self).setUp()
        load_fixture("provision-data")
        self.createUser()

    def test_new_file(self):
        utils._upload_file(self)

    def test_update_file(self):
        test_file = utils._upload_file(self)
        response = self.file_client.put('/file/' + test_file.hash,
                                        content_type='application/json',
                                        data={
                                            'name': 'NewFilename',
                                            'text': 'New Description',
                                        })
        assert_ok_response(response, OkMessage.Type.FILE_UPDATED)

    def test_delete_file(self):
        test_file = utils._upload_file(self)
        response = self.file_client.delete('/file/' + test_file.hash)
        assert_ok_response(response, OkMessage.Type.FILE_REMOVED)

    def test_get_file(self):
        test_file = utils._upload_file(self)
        response = self.file_client.delete('/file/' + test_file.hash)
        self.assertEqual(response.status_code, 200)

    def test_get_files_no_subject(self):
        try:
            utils._upload_file(self, level_id=1)
        except KeyError:
            pass
