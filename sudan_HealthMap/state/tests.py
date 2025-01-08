from django.test import TestCase
from state.models import State


class StateModelTest(TestCase):
    """
    Test cases for the State model.
    """

    def setUp(self):
        """
        Set up test data for the State model.
        """
        self.state = State.objects.create(name="Khartoum")

    def test_state_creation(self):
        """
        Test that a State instance is created successfully.
        """
        self.assertEqual(self.state.name, "Khartoum")
        self.assertEqual(str(self.state), "Khartoum")

    def test_duplicate_state_name(self):
        """
        Test that duplicate state names.
        """
        with self.assertRaises(Exception):
            State.objects.create(name="Khartoum")
