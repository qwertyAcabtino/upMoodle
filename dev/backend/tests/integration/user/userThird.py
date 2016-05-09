from rest.models.message.errorMessage import ErrorMessage

from tests.integration.auth.system import AuthenticationTestBase
from tests.utils import load_fixture, assert_error_response


class UserThirdTestCase(AuthenticationTestBase):

    def setUp(self):
        super(UserThirdTestCase, self).setUp()
        load_fixture("provision-data")
        self.createUser()

    def test_basic_getUser(self):
        self.login()
        pk = '1'
        response = self.client.get('/user/' + pk + '/')
        self.assertEqual(response.status_code, 200)

    def test_getUser_not_signed_in(self):
        self.logout()
        pk = '1'
        response = self.client.get('/user/' + pk + '/')
        assert_error_response(response, ErrorMessage.Type.NOT_SIGNED_IN)

    def test_getUser_id_overflow(self):
        self.login()
        pk = '191289347901273481236498712634971234123481263984'
        response = self.client.get('/user/' + pk + '/')
        assert_error_response(response, ErrorMessage.Type.INCORRECT_DATA)
