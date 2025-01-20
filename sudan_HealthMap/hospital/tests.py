from django.test import TestCase
from django.utils.timezone import now
from hospital.models import Hospital
from state.models import State
from supervisor.models import Supervisor


class HospitalModelTest(TestCase):
    """
    Test cases for the Hospital model.
    """

    @classmethod
    def setUpTestData(cls):
        """
        Set up test data for the hospital model.
        """
        cls.state = State.objects.create(name="Khartoum")

        cls.supervisor = Supervisor.objects.create_user(
            email="supervisor@example.com",
            name="John Doe",
            password="securepassword123"
        )

        cls.hospital = Hospital.objects.create(
            name="Sudan General Hospital",
            state=cls.state,
            supervisor=cls.supervisor,
            email="hospital@example.com",
            password="hospitalpassword123",
            last_login=now()
        )

    def test_hospital_creation(self):
        """
        Test the creation of a Hospital instance.
        """
        hospital = Hospital.objects.get(id=self.hospital.id)
        self.assertEqual(hospital.name, "Sudan General Hospital")
        self.assertEqual(hospital.state, self.state)
        self.assertEqual(hospital.supervisor, self.supervisor)
        self.assertEqual(hospital.email, "hospital@example.com")
        self.assertEqual(hospital.password, "hospitalpassword123")

    def test_hospital_is_authenticated(self):
        """
        Test the is_authenticated property of a Hospital.
        """
        self.assertTrue(self.hospital.is_authenticated)

    def test_last_login_field(self):
        """
        Test the last_login field.
        """
        self.assertIsNotNone(self.hospital.last_login)
