from django.test import TestCase

from upmoodle.models import ErrorMessage
from tests.utils import load_fixture


class ErrorMessageTestCase(TestCase):

    def setUp(self):
        load_fixture("provision-data")

    def test_errormessages_exists_in_db(self):
        self.assertEqual(len(ErrorMessage.objects.all()), 16)
