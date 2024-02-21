from django.test import TestCase, Client
from django.urls import reverse
from authentication.models import User
from django.contrib import auth
from django.test import TestCase, Client
from django.urls import reverse
from authentication.views import ProfileUpdateView
from authentication.forms import ProfileUpdateForm
from django.core.files.uploadedfile import SimpleUploadedFile


class ProfileUpdateViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword', bio='old bio')
        self.client.login(username='testuser', password='testpassword')

    def test_view_get(self):
        response = self.client.get(reverse('update_profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'update_profile.html')
        form = response.context['form']
        self.assertIsInstance(form, ProfileUpdateForm)
        self.assertEqual(form.initial.get('bio'), 'old bio')
        self.assertIsNone(form.initial.get('profile_pic.name'))

    def test_view_post_no_image(self):
        new_bio = 'new bio'
        response = self.client.post(reverse('update_profile'), {'bio': new_bio, 'profile_pic': ''})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('user_profile', args=[self.user.username]))
        self.user.refresh_from_db()
        self.assertEqual(self.user.bio, new_bio)
        self.assertEqual(self.user.profile_pic.name, '')

class TestViews(TestCase):

	# Setting up the Test-Data
	def setUp(self):
		# Create Test User
		self.user1 = User.objects.create(username='user1')
		self.user1.set_password('Testpw!')
		self.user1.save()

		# Create Client
		self.client = Client()

		# Set up Profile url
		self.profile_url = reverse('user_profile', args=['user1'])

	# Testing to get profile page when logged in
	def test_profile_get_logged_in(self):
		# Checking if User is logged in
		logged_in = self.client.login(username='user1', password='Testpw!')
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

class ProfileDeleteViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_delete_profile(self):
        # Log in the user
        self.client.login(username='testuser', password='testpassword')
        
        response = self.client.post(reverse('delete_profile', kwargs={'user_id': self.user.id}))
        
        # Check if the user is deleted
        self.assertEqual(User.objects.filter(username='testuser').count(), 0)
        
        # Check if the response redirects to the home page
        self.assertRedirects(response, reverse('home'))