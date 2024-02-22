from django.test import TestCase, Client
from django.urls import reverse
from authentication.models import User
from django.contrib import auth
from django.test import TestCase, Client  # noqa: F811
from django.urls import reverse  # noqa: F811
from authentication.forms import ProfileUpdateForm


class ProfileUpdateViewTest(TestCase):
    """
    Testcase to check the functionalites inside ProfileUpdateView
    """
    def setUp(self):
        """Setup Client and User. Logs user in."""
        self.client = Client()
        self.user = User.objects.create_user(username='testuser',
                                             password='testpassword',
                                             bio='old bio')
        self.client.login(username='testuser', password='testpassword')

    def test_view_get(self):
        """
        Tests if the correct view, form and data is returned from
        the ProfileUpdateView.
        """
        response = self.client.get(reverse('update_profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'update_profile.html')
        form = response.context['form']
        self.assertIsInstance(form, ProfileUpdateForm)
        self.assertEqual(form.initial.get('bio'), 'old bio')
        self.assertIsNone(form.initial.get('profile_pic.name'))

    def test_view_post_no_image(self):
        """
        Tests if the user bio can be updated.
        """
        new_bio = 'new bio'
        response = self.client.post(reverse('update_profile'),
                                    {'bio': new_bio,
                                    'profile_pic': ''})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('user_profile',
                         args=[self.user.username]))
        self.user.refresh_from_db()
        self.assertEqual(self.user.bio, new_bio)
        self.assertEqual(self.user.profile_pic.name, '')


class TestViews(TestCase):
    """
    Testcase to check User login and logout behaviour.
    """
    def setUp(self):
        """Create a Testuser"""
        self.user1 = User.objects.create(username='user1')
        self.user1.set_password('Testpw!')
        self.user1.save()

        # Create Client
        self.client = Client()

        # Set up Profile url
        self.profile_url = reverse('user_profile', args=['user1'])

    def test_profile_get_logged_in(self):
        """Testing to get profile page when logged in"""
        # Checking if User is logged in
        self.client.login(username='user1', password='Testpw!')
        user = auth.get_user(self.client)
        self.assertEqual(True, user.is_authenticated)

        # Testing profile View
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')

    def test_profile_get_logged_out(self):
        """Testing to get profile page when NOT logged in"""
        # Checking if User is logged out
        user = auth.get_user(self.client)
        self.assertEqual(False, user.is_authenticated)

        # Testing Profile View
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')


class ProfileDeleteViewTest(TestCase):
    """Testcase to check if a User is deleted succesfully on regquest."""
    def setUp(self):
        """Set up User account."""
        self.client = Client()
        self.user = User.objects.create_user(username='testuser',
                                             password='testpassword')

    def test_delete_profile(self):
        """Test deleting the user."""
        # Log in the user
        self.client.login(username='testuser', password='testpassword')

        # Delete User
        response = self.client.post(reverse('delete_profile',
                                            kwargs={'user_id': self.user.id}))

        # Check if the user is deleted
        self.assertEqual(User.objects.filter(username='testuser').count(), 0)

        # Check if the response redirects to the home page
        self.assertRedirects(response, reverse('home'))
