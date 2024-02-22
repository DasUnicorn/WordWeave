from django.test import TestCase, Client
from weave_manager.forms import ThreadForm, CommentForm
from weave_manager.models import Thread, Comment
from authentication.models import User


class ThreadFormTest(TestCase):
    """
    Testcase to test the creation of threads.
    """
    def setUp(self):
        """
        Set up the testuser and client.
        """
        self.user = User.objects.create_user(
            username='test', password='goodTesd123!')
        self.client = Client()

    def test_user_not_logged_in(self):
        """
        Test that no thread is created if the user is not logged in
        """
        form_data = {
            'title': 'Test Thread',
            'content': 'Test content for the thread',
            'tags': 'test, thread',
        }
        response = self.client.post('/create_thread', form_data)
        self.assertEqual(response.status_code, 302)  # Redirect to login page

    def test_valid_form(self):
        """
        Test form validation with a valid form.
        """
        form_data = {'title': 'Test Title',
                     'content': 'Test Content', 'tags': 'test_tag'}
        form = ThreadForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        """
        Test form validation with an invalid form.
        """
        form = ThreadForm(data={})  # Empty data should be invalid
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 3)

    def test_no_title_form(self):
        """
        Test form validation with an invalid form, missing a title.
        """
        form = ThreadForm(data={'content': 'Test Content', 'tags': 'test_tag'})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)

    def test_no_content_form(self):
        """
        Test form validation with an invalid form, missing the content.
        """
        form = ThreadForm(data={'title': 'Test Title', 'tags': 'test_tag'})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)

    def test_no_tag_form(self):
        """
        Test form validation with an invalid form, missing the tags.
        """
        form = ThreadForm(data={'title': 'Test Title',
                                'content': 'Test Content'})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)

    def test_long_title_form(self):
        """
        Test form validation with an invalid form, with a to long title.
        """
        form = ThreadForm(data={'title': 'Test Title'*100,
                                'content': 'Test Content', 'tags': 'test_tag'})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)

    def test_thread_form_submit(self):
        """
        Test the submit functionlity for valid forms.
        """
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
    """
    Testingt the Comment Form.
    """
    def setUp(self):
        """
        Set up a user and thread needed to create comments.
        """
        self.user = User.objects.create_user(
            username='test', password='goodTesd123!')
        self.thread = Thread.objects.create(
            title='Test Thread', content='Test content', author=self.user)

    def test_valid_comment_form(self):
        """
        Test a valid comment form.
        """
        form_data = {
            'body': 'Test comment body',
        }
        form = CommentForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_comment_form(self):
        """
        Test invalid (empty) comment form data.
        """
        form_data = {}
        form = CommentForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_comment_form_submit(self):
        """
        Test the comment form validation and
        form submision with valid form data.
        """
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
