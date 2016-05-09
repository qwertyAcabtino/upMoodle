from django.test import TestCase

from rest.models import OkMessage
from tests.utils import load_fixture


class OkMessageTestCase(TestCase):

    def setUp(self):
        load_fixture("provision-data")

    def test_message_exists_in_db(self):
        self.assertEqual(len(OkMessage.objects.all()), 16)
