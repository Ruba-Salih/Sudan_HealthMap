from django.test import TestCase
from supervisor.models import Supervisor


class SupervisorModelTest(TestCase):
    def setUp(self):
        """
        Set up test data for the Supervisor model.
        """
        self.supervisor_data = {
            'email': 'test_supervisor@example.com',
            'name': 'Test Supervisor',
            'password': 'password123',
        }

        self.supervisor = Supervisor.objects.create_user(
            email=self.supervisor_data['email'],
            name=self.supervisor_data['name'],
            password=self.supervisor_data['password'],
        )

    def test_create_user(self):
        """
        Test creating a normal supervisor user.
        """
        self.assertEqual(self.supervisor.email, self.supervisor_data['email'])
        self.assertEqual(self.supervisor.name, self.supervisor_data['name'])
        self.assertTrue(self.supervisor.is_active)
        self.assertFalse(self.supervisor.is_staff)
        self.assertFalse(self.supervisor.is_superuser)

    def test_create_superuser(self):
        """
        Test creating a superuser.
        """
        superuser = Supervisor.objects.create_superuser(
            email='superuser@example.com',
            name='Super User',
            password='superpassword',
        )
        self.assertEqual(superuser.email, 'superuser@example.com')
        self.assertEqual(superuser.name, 'Super User')
        self.assertTrue(superuser.is_active)
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)

    def test_get_full_name(self):
        """
        Test the get_full_name method.
        """
        self.assertEqual(self.supervisor.get_full_name(), self.supervisor_data['name'])

    def test_user_without_emai(self):
        """
        Test creating a user without an email.
        """
        with self.assertRaises(ValueError):
            Supervisor.objects.create_user(
                email=None,
                name='No Email User',
                password='password123',
            )
