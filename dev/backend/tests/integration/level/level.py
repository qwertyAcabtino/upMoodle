from django.test import TestCase

from rest.models import Level
from tests.utils import load_fixture


class LevelTestCase(TestCase):

    def setUp(self):
        load_fixture("provision-data")

    def test_level_exits_in_db(self):
        self.assertEqual(len(Level.objects.all()), 7)
