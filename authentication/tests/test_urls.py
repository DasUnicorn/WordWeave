from django.test import SimpleTestCase
from django.urls import reverse, resolve
from authentication.views import UserProfileView, ProfileUpdateView

# Url Testcases
class TestUrls(SimpleTestCase):

	# Test-case to check if the user profile url resoves correctly
	def test_url_profile_is_resolved(self):
		url = reverse('user_profile', args=['user'])
		self.assertEqual(resolve(url).func.view_class, UserProfileView)

	# Test-case to check if the profile setting url resoves correctly
	def test_url_profile_setting_is_resolved(self):
		url = reverse('update_profile')
		self.assertEqual(resolve(url).func.view_class, ProfileUpdateView)