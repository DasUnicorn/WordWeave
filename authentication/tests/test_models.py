from django.test import TestCase, Client
from django.urls import reverse
from authentication.models import User

class TestModals(TestCase):

	# Set up user info, for further test cases
	def setUp(self):
		self.user1 = User.objects.create(
			username = 'Salbei',
			bio = 'This is a bio.',
			email = 'test@test.de'
			)