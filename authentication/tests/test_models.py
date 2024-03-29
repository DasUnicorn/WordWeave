from django.test import TestCase
from authentication.models import User


class TestModals(TestCase):
    """
    Testcase for models in authenticator app.
    """
    def setUp(self):
        """Set up user info for further testing."""
        self.username = 'Salbei'
        self.bio = 'This is a bio.'
        self.email = 'test@test.de'

    def test_user_creation(self):
        """
        Test Creating a user instance.
        """
        user = User.objects.create(
            username=self.username,
            bio=self.bio,
            email=self.email
        )

        # Assert that the user object is created successfully
        self.assertIsNotNone(user)

        # Assert that the attributes of the user object
        # match the expected values
        self.assertEqual(user.username, self.username)
        self.assertEqual(user.bio, self.bio)
        self.assertEqual(user.email, self.email)
