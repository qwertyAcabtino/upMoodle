from upmoodle.models import FileType
from tests.integration.auth.system import AuthenticationTestBase
from tests.utils import load_fixture


class FileTypeTestCase(AuthenticationTestBase):

    def setUp(self):
        load_fixture("provision-data")

    def test_levelTypes_exits_in_db(self):
        self.assertEqual(len(FileType.objects.all()), 6)

