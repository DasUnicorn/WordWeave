from django.test import TestCase, Client
from django.urls import reverse
from authentication.models import User
from weave_manager.models import Thread
from django.template.response import TemplateResponse


class InfoViewTest(TestCase):
    """Unittest to test the Info View."""
    def setUp(self):
        """Set up the Client"""
        self.client = Client()

    def test_info_view(self):
        """
        Tests if the info site is reached by the correct url
        with the correct template.
        """
        url = reverse('info')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response, TemplateResponse)
        self.assertTemplateUsed(response, 'info.html')


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser', password='testpaswort123!')
        self.thread = Thread.objects.create(
            title='Test Thread', author=self.user, content='Test Content')

    def test_global_timeline_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_create_thread_view(self):
        self.client.login(username='testuser', password='testpaswort123!')
        response = self.client.post(reverse('create_thread'), {
            'title': 'New Thread',
            'content': 'New Content'
        })
        self.assertEqual(response.status_code, 200)

    def test_thread_detail_view(self):
        response = self.client.get(
            reverse('thread_detail', args=(self.thread.id, self.thread.slug)))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'thread_detail.html')
        self.assertIn(self.thread.title, response.content.decode())


class ThreadEditTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')
        self.thread = Thread.objects.create(
            title='Test Thread', content='Original content', tags='test',
            author=self.user)

    def test_thread_edit(self):
        # Log in as the user
        self.client.login(username='testuser', password='testpassword')

        # New content for the thread
        new_content = 'Updated content'

        # Send a POST request to edit the thread
        response = self.client.post(
            reverse('edit_thread', kwargs={'thread_id': self.thread.id}),
            # Include new content in the POST data
            data={'title': self.thread.title,
                  'content': new_content, 'tags': self.thread.tags}
        )

        # Check that the thread's content is updated correct
        self.thread.refresh_from_db()
        self.assertEqual(self.thread.content, new_content)

        # Check that redirect after editing
        self.assertEqual(response.status_code, 302)

        # Check that the redirect is to the correct site
        redirected_url = response.url
        expected_url = reverse('thread_detail', kwargs={
            'thread_id': self.thread.id, 'slug': self.thread.slug})
        self.assertEqual(redirected_url, expected_url)
