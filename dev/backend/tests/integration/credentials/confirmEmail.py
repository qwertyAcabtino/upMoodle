import json

from rest.models import User, ErrorMessage
from rest.models.message.errorMessage import ErrorMessageType
from tests.integration.system import AuthenticationTestBase
from tests.utils import load_fixture, assert_error_response


class ConfirmEmailTestCase(AuthenticationTestBase):

    def setUp(self):
        super(ConfirmEmailTestCase, self).setUp()
        load_fixture("provision-data")
        self.createUser()
        user = User.objects.get(id=1)
        user.confirmedEmail = False
        user.save()

    def test_1_basic_confirm(self):
        user = User.objects.get(id=1)
        response = self.client.post('/confirm_email/', {'token': user.sessionToken})
        self.assertEqual(response.status_code, 200)
        user = User.objects.get(id=1)
        self.assertTrue(user.confirmedEmail)

    def test_2_already_confirmed(self):
        user = User.objects.get(id=1)
        user.confirmedEmail = True
        user.save()

        response = self.client.post('/confirm_email/', {'token': user.sessionToken})
        assert_error_response(response, ErrorMessageType.ALREADY_CONFIRMED)

    def test_3_invalid_token(self):
        response = self.client.post('/confirm_email/', {'token': 'randomdata'})
        assert_error_response(response, ErrorMessageType.INCORRECT_DATA)

    def test_4_long_token(self):
        response = self.client.post('/confirm_email/', {
            'token': '/confirm_email/.eJxVjEEOwiAQRe8ya0MgpKV06d4zEIaZ2oqBBGi6MN5dTLrQ7fvv_Rc4v7fV7ZWLW31dYQa0rKWeFoNGB2UJB5r0oEhKo3gZ0dpx0tYvcIHGtYWc48a9O3KJTJ3-XG4Es_oj6EPk1DHQw6d7FiGnVjYUX0WcaxW3TPy8nu77A9mHOJM:1Xpov5:Bnfuxp-BIVKSwSsUv7msEffLK70adfsalsldflkasdjflaksjdflkasdjfkasdasdfhasdfasjdfijaosdifjaosidff/'})
        assert_error_response(response, ErrorMessageType.INCORRECT_DATA)
