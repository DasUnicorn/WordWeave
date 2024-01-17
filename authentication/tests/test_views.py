from django.test import TestCase, Client
from django.urls import reverse
from authentication.models import User
from django.contrib import auth
import json

class TestViews(TestCase):

	# Setting up the Test-Data
	def setUp(self):
		# Create Test User
		self.user1 = User.objects.create(username='user1')
		self.user1.set_password('testpw!')
		self.user1.save()

		# Create Client
		self.client = Client()

		# Set up Profile url
		self.profile_url = reverse('user_profile', args=['user1'])

	# Testing to get profile page when logged in
	def test_profile_get_logged_in(self):
		# Checking if User is logged in
		logged_in = self.client.login(username='user1', password='testpw!')
		user = auth.get_user(self.client)
		self.assertEqual(True, user.is_authenticated)

		# Testing profile View
		response = self.client.get(self.profile_url)
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'profile.html')

	# Testing to get profile page when NOT logged in
	def test_profile_get_logged_out(self):
		# Checking if User is logged out
		user = auth.get_user(self.client)
		self.assertEqual(False, user.is_authenticated)

		# Testing Profile View
		response = self.client.get(self.profile_url)
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'profile.html')