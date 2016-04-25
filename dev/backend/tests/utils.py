import json
import string

from django.core.management import call_command
from django.utils.crypto import random

from rest.models import ErrorMessage, Message


def load_fixture(fixture_name):
    call_command("loaddata", "ddbb/"+fixture_name+".json", verbosity=0)


def assert_error_response(response, error_type):
    error = ErrorMessage.objects.get(pk=error_type.value)
    decoded = json.loads(response.content)

    assert response.status_code == error.http_code
    try:
        assert error.error == decoded['error']
    except AssertionError:
        assert (error.error in decoded['error'])


def assert_ok_response(response, ok_type):
    message = Message.objects.get(pk=ok_type.value)
    decoded = json.loads(response.content)

    assert message.message == decoded['message']


def get_random_string(length):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(length))
