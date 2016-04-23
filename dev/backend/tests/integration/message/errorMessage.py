from django.test import TestCase

from rest.models import ErrorMessage
from tests.utils import load_fixture


class ErrorMessageTestCase(TestCase):

    def setUp(self):
        load_fixture("provision-data")

    def test_errormessages_exists_in_db(self):
        # ErrorMessage.objects.create(error="Request cannot be performed", http_code=400)
        # ErrorMessage.objects.create(error="Incorrect data", http_code=400)
        # ErrorMessage.objects.create(error="Cookies are disabled", http_code=400)
        # ErrorMessage.objects.create(error="Already confirmed", http_code=400)
        # ErrorMessage.objects.create(error="Invalid token", http_code=400)
        # ErrorMessage.objects.create(error="User already in use", http_code=400)
        # ErrorMessage.objects.create(error="Unauthorized", http_code=400)
        # ErrorMessage.objects.create(error="Incorrect file data", http_code=400)
        # ErrorMessage.objects.create(error="Password's length has to be between 8 and 100", http_code=400)
        # ErrorMessage.objects.create(error="Nickname's length has to be between 4 and 20", http_code=400)
        # ErrorMessage.objects.create(error="Email field cannot be empty", http_code=400)
        # ErrorMessage.objects.create(error="Please, check your inbox and confirm your email.", http_code=400)
        # ErrorMessage.objects.create(error="Please, sign in first.", http_code=400)
        # ErrorMessage.objects.create(error="Name's length has to be between 4 and 100", http_code=400)
        # ErrorMessage.objects.create(error="Invalid level", http_code=400)
        self.assertEqual(len(ErrorMessage.objects.all()), 15)
