from rest.models import User
from tests.integration.system import AuthenticationTestBase
from tests.utils import load_fixture


class EditSubjectsTestCase(AuthenticationTestBase):

    def setUp(self):
        super(EditSubjectsTestCase, self).setUp()
        load_fixture("provision-data")
        self.createUser()

    def test_1_editSubjects_basic(self):
        self.login()
        response = self.client.post('/user/subjects/', {'ids': [5, 6]})
        self.assertEqual(response.status_code, 200)
        userUpdated = User.objects.get(id=1)
        self.assertEqual(len(userUpdated.subjects.all()), 2)

    def test_2_editSubjects_basic(self):
        self.login()

        response = self.client.post('/user/subjects/', {'ids': [5, 6, 4]})
        self.assertEqual(response.status_code, 200)
        userUpdated = User.objects.get(id=1)
        self.assertEqual(len(userUpdated.subjects.all()), 3)

    def test_3_editSubjects_empty(self):
        self.login()
        response = self.client.post('/user/subjects/', {'ids': []})
        self.assertEqual(response.status_code, 200)
        userUpdated = User.objects.get(id=1)
        self.assertEqual(len(userUpdated.subjects.all()), 0)

    def test_4_editSubjects_empty(self):
        self.login()
        response = self.client.post('/user/subjects/', {'ids': []})
        self.assertEqual(response.status_code, 200)
        userUpdated = User.objects.get(id=1)
        self.assertEqual(len(userUpdated.subjects.all()), 0)

    def test_5_editSubjects_empty(self):
        self.login()
        response = self.client.post('/user/subjects/', {'ids': [5,6]})
        response = self.client.post('/user/subjects/', {})
        self.assertEqual(response.status_code, 400)
        userUpdated = User.objects.get(id=1)
        self.assertEqual(len(userUpdated.subjects.all()), 2)

    def test_6_editSubjects_notSubjects(self):
        self.login()
        response = self.client.post('/user/subjects/', {'ids': []})
        userUpdated = User.objects.get(id=1)
        self.assertEqual(len(userUpdated.subjects.all()), 0)
        self.assertEqual(response.status_code, 200)
        response = self.client.post('/user/subjects/', {'ids': [1, 5, 6]})
        self.assertEqual(response.status_code, 400)
        userUpdated = User.objects.get(id=1)
        self.assertEqual(len(userUpdated.subjects.all()), 0)
        self.assertEqual(len(userUpdated.subjects.all()), 0)