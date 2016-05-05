from rest.models import User
from tests.integration.system import AuthenticationTestBase
from tests.utils import load_fixture


class EditSubjectsTestCase(AuthenticationTestBase):

    def setUp(self):
        super(EditSubjectsTestCase, self).setUp()
        load_fixture("provision-data")
        self.createUser()

    def test_editSubjects_basic(self):
        self.login()
        response = self.client.post('/user/subjects/', {'ids': [5, 6]})
        self.assertEqual(response.status_code, 200)
        updated_user = User.objects.get(id=1)
        self.assertEqual(len(updated_user.subjects.all()), 2)

    def test_editSubjects_basic_2(self):
        self.login()

        response = self.client.post('/user/subjects/', {'ids': [5, 6, 4]})
        self.assertEqual(response.status_code, 200)
        updated_user = User.objects.get(id=1)
        self.assertEqual(len(updated_user.subjects.all()), 3)

    def test_editSubjects_empty(self):
        self.login()
        response = self.client.post('/user/subjects/', {'ids': []})
        self.assertEqual(response.status_code, 200)
        updated_user = User.objects.get(id=1)
        self.assertEqual(len(updated_user.subjects.all()), 0)

    def test_editSubjects_empty_2(self):
        self.login()
        response = self.client.post('/user/subjects/', {'ids': []})
        self.assertEqual(response.status_code, 200)
        updated_user = User.objects.get(id=1)
        self.assertEqual(len(updated_user.subjects.all()), 0)

    def test_editSubjects_empty_3(self):
        self.login()
        self.client.post('/user/subjects/', {'ids': [5, 6]})
        response = self.client.post('/user/subjects/', {})
        self.assertEqual(response.status_code, 400)
        updated_user = User.objects.get(id=1)
        self.assertEqual(len(updated_user.subjects.all()), 2)

    def test_editSubjects_notSubjects(self):
        self.login()
        response = self.client.post('/user/subjects/', {'ids': []})
        updated_user = User.objects.get(id=1)
        self.assertEqual(len(updated_user.subjects.all()), 0)
        self.assertEqual(response.status_code, 200)
        response = self.client.post('/user/subjects/', {'ids': [1, 5, 6]})
        self.assertEqual(response.status_code, 400)
        updated_user = User.objects.get(id=1)
        self.assertEqual(len(updated_user.subjects.all()), 0)
        self.assertEqual(len(updated_user.subjects.all()), 0)
