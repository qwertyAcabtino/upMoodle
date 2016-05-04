from tests.integration.system import AuthenticationTestBase
from tests.utils import load_fixture


class LogoutTestCase(AuthenticationTestBase):

    def setUp(self):
        super(LogoutTestCase, self).setUp()
        load_fixture("provision-data")
        self.createUser()

    def test_1_logout_basic(self):
        response = self.client.post('/logout/')
        self.assertEqual(response.status_code, 200)

