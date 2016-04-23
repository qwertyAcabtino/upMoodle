from django.test import TestCase

from rest.models import Message
from tests.utils import load_fixture


class MessageTestCase(TestCase):

    def setUp(self):
        load_fixture("provision-data")

    def test_message_exists_in_db(self):
        self.assertEqual(len(Message.objects.all()), 14)
