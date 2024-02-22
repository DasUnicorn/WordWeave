from django.test import SimpleTestCase
from django.urls import reverse, resolve
from authentication.views import UserProfileView, ProfileUpdateView


class TestUrls(SimpleTestCase):
    """
    Testcase to test the URls in app authentication.
    """

    def test_url_profile_is_resolved(self):
        """
        Test-case to check if the user profile url resoves correctly.
        """
        url = reverse('user_profile', args=['user'])
        self.assertEqual(resolve(url).func.view_class, UserProfileView)

    def test_url_profile_setting_is_resolved(self):
        """
        Test-case to check if the profile setting url resoves correctly.
        """
        url = reverse('update_profile')
        self.assertEqual(resolve(url).func.view_class, ProfileUpdateView)
