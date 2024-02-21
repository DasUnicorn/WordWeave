from django.test import TestCase, Client
from weave_manager.forms import ThreadForm, CommentForm
from weave_manager.models import Thread, Comment
from authentication.models import User


class ThreadFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='test', password='goodTesd123!')
        self.client = Client()

    def test_user_not_logged_in(self):
        # Test that no thread is created if the user is not logged in
        form_data = {
            'title': 'Test Thread',
            'content': 'Test content for the thread',
            'tags': 'test, thread',
        }
        response = self.client.post('/create_thread', form_data)
        self.assertEqual(response.status_code, 302)  # Redirect to login page

    def test_valid_form(self):
        form_data = {'title': 'Test Title',
                     'content': 'Test Content', 'tags': 'test_tag'}
        form = ThreadForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        form = ThreadForm(data={})  # Empty data should be invalid
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 3)

    def test_no_title_form(self):
        form = ThreadForm(data={'content': 'Test Content', 'tags': 'test_tag'})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)

    def test_no_content_form(self):
        form = ThreadForm(data={'title': 'Test Title', 'tags': 'test_tag'})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)

    def test_no_tag_form(self):
        form = ThreadForm(data={'title': 'Test Title',
                                'content': 'Test Content'})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)

    def test_long_title_form(self):
        form = ThreadForm(data={'title': 'Test Title'*100,
                                'content': 'Test Content', 'tags': 'test_tag'})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)

    def test_thread_form_submit(self):
        form_data = {
            'title': 'Test Title',
            'content': 'Test Content',
            'tags': 'test'
        }
        form = ThreadForm(data=form_data)
        self.assertTrue(form.is_valid())
        # Saving the form data
        thread = form.save(commit=False)
        thread.author = self.user
        thread.save()
        # Check if the thread was saved successfully
        self.assertIsNotNone(Thread.objects.get(title='Test Title'))


class CommentFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='test', password='goodTesd123!')
        self.thread = Thread.objects.create(
            title='Test Thread', content='Test content', author=self.user)

    def test_valid_comment_form(self):
        form_data = {
            'body': 'Test comment body',
        }
        form = CommentForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_comment_form(self):
        # Testing invalid form data
        form_data = {}  # Empty data should make the form invalid
        form = CommentForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_comment_form_submit(self):
        form_data = {
            'body': 'Test comment body',
        }
        form = CommentForm(data=form_data)
        self.assertTrue(form.is_valid())
        # Saving the form data
        comment = form.save(commit=False)
        comment.author = self.user
        comment.thread = self.thread
        comment.save()
        # Check if the comment was saved successfully
        self.assertIsNotNone(Comment.objects.get(body='Test comment body'))
