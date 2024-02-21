from django.test import TestCase
from authentication.models import User
from django.urls import reverse
from weave_manager.models import Thread, Comment, ThreadVote, CommentVote


class ThreadVoteTest(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username='testuser', password='Pass123Word!')
        # Create a test thread
        self.thread = Thread.objects.create(
            title='Test Thread', content='Test Content', author=self.user)

    def test_upvote_thread(self):
        # Log in the user
        self.client.login(username='testuser', password='Pass123Word!')
        # Send a POST request to upvote the thread
        response = self.client.post(
            reverse('upvote_thread', kwargs={'thread_id': self.thread.id}))
        # Check if the response is a redirect
        self.assertEqual(response.status_code, 302)
        # Follow the redirect
        redirected_response = self.client.get(response.url)
        # Check if the redirected response is successful
        self.assertEqual(redirected_response.status_code, 200)
        # Check if the thread has received an upvote
        self.thread.refresh_from_db()
        self.assertEqual(self.thread.votes, 1)

    def test_downvote_thread(self):
        # Log in the user
        self.client.login(username='testuser', password='Pass123Word!')
        # Send a POST request to downvote the thread
        response = self.client.post(
            reverse('downvote_thread', kwargs={'thread_id': self.thread.id}))
        # Check if the response is a redirect
        self.assertEqual(response.status_code, 302)
        # Follow the redirect
        redirected_response = self.client.get(response.url)
        # Check if the redirected response is successful
        self.assertEqual(redirected_response.status_code, 200)
        # Check if the thread has received a downvote
        self.thread.refresh_from_db()
        self.assertEqual(self.thread.votes, -1)

    def test_change_upvote_to_downvote(self):
        # Log in the user
        self.client.login(username='testuser', password='Pass123Word!')
        # Upvote the thread
        self.client.post(reverse('upvote_thread', kwargs={'thread_id': self.thread.id}))
        # Check if the thread has received an upvote
        self.thread.refresh_from_db()
        self.assertEqual(self.thread.votes, 1)
        # Send a POST request to change the vote to downvote
        response = self.client.post(reverse('downvote_thread', kwargs={'thread_id': self.thread.id}))
        # Check if the response is a redirect
        self.assertEqual(response.status_code, 302)
        # Follow the redirect
        redirected_response = self.client.get(response.url)
        # Check if the redirected response is successful
        self.assertEqual(redirected_response.status_code, 200)
        # Check if the thread has received a downvote
        self.thread.refresh_from_db()
        self.assertEqual(self.thread.votes, -1)

    def test_change_downvote_to_upvote(self):
        # Log in the user
        self.client.login(username='testuser', password='Pass123Word!')
        # Downvote the thread
        self.client.post(reverse('downvote_thread', kwargs={'thread_id': self.thread.id}))
        # Check if the thread has received a downvote
        self.thread.refresh_from_db()
        self.assertEqual(self.thread.votes, -1)
        # Send a POST request to change the vote to upvote
        response = self.client.post(reverse('upvote_thread', kwargs={'thread_id': self.thread.id}))
        # Check if the response is a redirect
        self.assertEqual(response.status_code, 302)
        # Follow the redirect
        redirected_response = self.client.get(response.url)
        # Check if the redirected response is successful
        self.assertEqual(redirected_response.status_code, 200)
        # Check if the thread has received an upvote
        self.thread.refresh_from_db()
        self.assertEqual(self.thread.votes, 1)


class CommentVoteTest(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username='testuser', password='Pass123Word!')
        # Create a test thread
        self.thread = Thread.objects.create(
            title='Test Thread', content='Test Content', author=self.user)
        # Create a test comment on the thread
        self.comment = Comment.objects.create(
            body='This is a Test.', author=self.user, thread=self.thread)

    def test_upvote_comment(self):
        # Log in the user
        self.client.login(username='testuser', password='Pass123Word!')
        # Send a POST request to upvote the comment
        response = self.client.post(
            reverse('upvote_comment', kwargs={'comment_id': self.comment.id}))
        # Check if the response is a redirect
        self.assertEqual(response.status_code, 302)
        # Follow the redirect
        redirected_response = self.client.get(response.url)
        # Check if the redirected response is successful
        self.assertEqual(redirected_response.status_code, 200)
        # Check if the comment has received an upvote
        self.comment.refresh_from_db()
        self.assertEqual(self.comment.votes, 1)

    def test_downvote_comment(self):
        # Log in the user
        self.client.login(username='testuser', password='Pass123Word!')
        # Send a POST request to downvote the comment
        response = self.client.post(
            reverse('downvote_comment', kwargs={'comment_id': self.comment.id}))
        # Check if the response is a redirect
        self.assertEqual(response.status_code, 302)
        # Follow the redirect
        redirected_response = self.client.get(response.url)
        # Check if the redirected response is successful
        self.assertEqual(redirected_response.status_code, 200)
        # Check if the comment has received a downvote
        self.comment.refresh_from_db()
        self.assertEqual(self.comment.votes, -1)

    def test_change_upvote_to_downvote(self):
        # Log in the user
        self.client.login(username='testuser', password='Pass123Word!')
        # Upvote the comment
        self.client.post(reverse('upvote_comment', kwargs={'comment_id': self.comment.id}))
        # Check if the comment has received an upvote
        self.comment.refresh_from_db()
        self.assertEqual(self.comment.votes, 1)
        # Send a POST request to change the vote to downvote
        response = self.client.post(reverse('downvote_comment', kwargs={'comment_id': self.comment.id}))
        # Check if the response is a redirect
        self.assertEqual(response.status_code, 302)
        # Follow the redirect
        redirected_response = self.client.get(response.url)
        # Check if the redirected response is successful
        self.assertEqual(redirected_response.status_code, 200)
        # Check if the comment has received a downvote
        self.comment.refresh_from_db()
        self.assertEqual(self.comment.votes, -1)

    def test_change_downvote_to_upvote(self):
        # Log in the user
        self.client.login(username='testuser', password='Pass123Word!')
        # Downvote the comment
        self.client.post(reverse('downvote_comment', kwargs={'comment_id': self.comment.id}))
        # Check if the comment has received a downvote
        self.comment.refresh_from_db()
        self.assertEqual(self.comment.votes, -1)
        # Send a POST request to change the vote to upvote
        response = self.client.post(reverse('upvote_comment', kwargs={'comment_id': self.comment.id}))
        # Check if the response is a redirect
        self.assertEqual(response.status_code, 302)
        # Follow the redirect
        redirected_response = self.client.get(response.url)
        # Check if the redirected response is successful
        self.assertEqual(redirected_response.status_code, 200)
        # Check if the comment has received an upvote
        self.comment.refresh_from_db()
        self.assertEqual(self.comment.votes, 1)


class ThreadVoteDeletionTest(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username='testuser', password='Pass123Word!')
        # Create a test thread
        self.thread = Thread.objects.create(
            title='Test Thread', content='Test Content', author=self.user)
        # Log in the user
        self.client.login(username='testuser', password='Pass123Word!')
        # Upvote the thread
        self.client.post(reverse('upvote_thread', kwargs={
                         'thread_id': self.thread.id}))

    def test_vote_deletion(self):
        # Get the vote associated with the thread
        vote = ThreadVote.objects.get(user=self.user, thread=self.thread)
        # Delete the vote
        vote.delete()
        # Refresh the thread from the database
        self.thread.refresh_from_db()
        # Check if the vote object is deleted
        self.assertFalse(ThreadVote.objects.filter(id=vote.id).exists())
        # Check if the vote count of the thread is adjusted accordingly
        self.assertEqual(self.thread.votes, 0)


class CommentVoteDeletionTest(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username='testuser', password='Pass123Word!')
        # Create a test thread
        self.thread = Thread.objects.create(
            title='Test Thread', content='Test Content', tags='test', author=self.user)
        # Create a test comment to the thread
        self.comment = Comment.objects.create(
            body='This is a Test.', author=self.user, thread=self.thread)
        # Log in the user
        self.client.login(username='testuser', password='Pass123Word!')
        # Upvote the comment
        self.client.post(reverse('upvote_comment', kwargs={
                         'comment_id': self.comment.id}))

    def test_vote_deletion(self):
        # Get the vote associated with the thread
        vote = CommentVote.objects.get(user=self.user, comment=self.comment)
        # Delete the vote
        vote.delete()
        # Refresh the thread from the database
        self.comment.refresh_from_db()
        # Check if the vote object is deleted
        self.assertFalse(CommentVote.objects.filter(id=vote.id).exists())
        # Check if the vote count of the thread is adjusted accordingly
        self.assertEqual(self.comment.votes, 0)


class UniqueThreadVoteTest(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username='testuser', password='Pass123Word!')
        # Create a test thread
        self.thread = Thread.objects.create(
            title='Test Thread', content='Test Content', tags='test', author=self.user)
        # Log in the user
        self.client.login(username='testuser', password='Pass123Word!')

    def test_unique_vote(self):
        # Upvote the thread
        response = self.client.post(
            reverse('upvote_thread', kwargs={'thread_id': self.thread.id}))
        # Check if the thread has received an upvote
        self.thread.refresh_from_db()
        self.assertEqual(self.thread.votes, 1)

        # Attempt to upvote the thread again
        response = self.client.post(
            reverse('upvote_thread', kwargs={'thread_id': self.thread.id}))
        # Check if the previous vote is removed and the vote count is back to 0
        self.thread.refresh_from_db()
        self.assertEqual(self.thread.votes, 0)


class UniqueCommentVoteTest(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username='testuser', password='Pass123Word!')
        # Create a test thread
        self.thread = Thread.objects.create(
            title='Test Thread', content='Test Content', tags='test', author=self.user)
        # Create a test comment to the thread
        self.comment = Comment.objects.create(
            body='This is a Test.', author=self.user, thread=self.thread)
        # Log in the user
        self.client.login(username='testuser', password='Pass123Word!')

    def test_unique_vote(self):
        # Upvote the thread
        response = self.client.post(
            reverse('upvote_comment', kwargs={'comment_id': self.comment.id}))
        # Check if the thread has received an upvote
        self.comment.refresh_from_db()
        self.assertEqual(self.comment.votes, 1)

        # Attempt to upvote the comment again
        response = self.client.post(
            reverse('upvote_comment', kwargs={'comment_id': self.comment.id}))
        # Check if the previous vote is removed and the vote count is back to 0
        self.comment.refresh_from_db()
        self.assertEqual(self.comment.votes, 0)
