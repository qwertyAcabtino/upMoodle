from upmoodle.models import Rol
from upmoodle.models.message.errorMessage import ErrorMessage

from tests.integration.auth.system import AuthenticationTestBase
from tests.utils import load_fixture, assert_error_response


class RolUsersTestCase(AuthenticationTestBase):

    def setUp(self):
        super(RolUsersTestCase, self).setUp()
        load_fixture("provision-data")
        self.createUser()

    def test_basic_usersRol(self):
        self.login()
        rol = Rol.objects.get(name='Alumno')
        response = self.client.get('/rol/student/users')
        self.assertEqual(response.status_code, 200)

    def test_usersRol_not_signedIn(self):
        self.logout()
        rol = Rol.objects.get(name='Alumno')
        response = self.client.get('/rol/' + str(rol.id) + '/users')
        assert_error_response(response, ErrorMessage.Type.NOT_SIGNED_IN)