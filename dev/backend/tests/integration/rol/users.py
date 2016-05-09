from rest.models import Rol
from rest.models.message.errorMessage import ErrorMessage

from tests.integration.system import AuthenticationTestBase
from tests.utils import load_fixture, assert_error_response


class RolUsersTestCase(AuthenticationTestBase):

    def setUp(self):
        super(RolUsersTestCase, self).setUp()
        load_fixture("provision-data")
        self.createUser()

    def test_basic_usersRol(self):
        self.login()
        rol = Rol.objects.get(name='Alumno')
        response = self.client.get('/rol/' + str(rol.id) + '/users')
        self.assertEqual(response.status_code, 200)

    def test_usersRol_not_signedIn(self):
        self.logout()
        rol = Rol.objects.get(name='Alumno')
        response = self.client.get('/rol/' + str(rol.id) + '/users')
        assert_error_response(response, ErrorMessage.Type.NOT_SIGNED_IN)

    def test_userRol_id_overflow(self):
        self.login()
        rol = '191289347901273481236498712634971234123481263984'
        response = self.client.get('/rol/' + rol + '/users')
        assert_error_response(response, ErrorMessage.Type.INCORRECT_DATA)
