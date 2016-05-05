import json

from django.test import TestCase

from rest.models import Rol
from tests.integration.system import AuthenticationTestBase
from tests.utils import load_fixture


class RolTestCase(TestCase):

    def setUp(self):
        load_fixture("provision-data")

    def test_roles_exits_in_db(self):
        self.assertEqual(len(Rol.objects.all()), 6)


class RolEndpointTestCase(AuthenticationTestBase):

    def setUp(self):
        super(RolEndpointTestCase, self).setUp()
        load_fixture("provision-data")
        self.createUser()

    def test_get_all_roles(self):
        self.login()
        response = self.client.get('/rol/_all')
        data = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), 6)
