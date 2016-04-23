from django.test import TestCase

from rest.models import Rol
from tests.utils import load_fixture


class RolTestCase(TestCase):

    def setUp(self):
        load_fixture("provision-data")

    def test_roles_exits_in_db(self):
        self.assertEqual(len(Rol.objects.all()), 6)
