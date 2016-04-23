from django.test import TestCase

from rest.models import LevelType
from tests.utils import load_fixture


class LevelTypeTestCase(TestCase):

    def setUp(self):
        load_fixture("provision-data")

    def test_levelTypes_exits_in_db(self):
        self.assertEqual(len(LevelType.objects.all()), 5)
