from django.test import TestCase, Client
from django.urls import reverse
from authentication.models import User
import json

class TestViews(TestCase):

	# Setting up the Test-Data
	def setUp(self):
		self.client = Client()
		self.user1 = User.objects.create(
			username = 'user1',
			bio = 'This is my bio.'
			)
		self.profile_url = reverse('user_profile', kwargs={'username': 'user1'})

	# Testing to get profile page
	def test_profile_GET(self):
		response = self.client.get(self.profile_url)

		self.assertEqual(response.status_code, 200)
		self.asserrTemplateUsed(response, 'authentication/templates/profile.html')