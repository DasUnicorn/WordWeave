from django.test import TestCase
from authentication.models import User
from weave_manager.models import Thread, Comment, ThreadVote, CommentVote

class ThreadModelTest(TestCase):
    def setUp(self):
        # Create a user
        self.user = User.objects.create(username='testuser', password='Pass123Word!')
        # Create tags
        self.tag1 = "tag1"
        self.tag2 = "tag2"
        # Create a thread
        self.thread = Thread.objects.create(title='Test Thread', content='Test Content', author=self.user)
        self.thread.tags.add(self.tag1, self.tag2)

    def test_thread_creation(self):
        self.assertEqual(Thread.objects.count(), 1)
        self.assertEqual(self.thread.title, 'Test Thread')
        self.assertEqual(self.thread.content, 'Test Content')
        self.assertEqual(self.thread.author, self.user)
        self.assertEqual(self.thread.votes, 0)
        self.assertEqual(set(self.thread.tags.names()), set([self.tag1, self.tag2]))

    def test_thread_up_vote(self):
        # Upvote the thread
        self.thread.up_vote(self.user)
        # Retrieve the updated thread from the database
        updated_thread = Thread.objects.get(id=self.thread.id)
        self.assertEqual(updated_thread.votes, 1)
        self.assertTrue(updated_thread.has_upvoted(self.user))

    def test_thread_down_vote(self):
        # Downvote the thread
        self.thread.down_vote(self.user)
        # Retrieve the updated thread from the database
        updated_thread = Thread.objects.get(id=self.thread.id)
        self.assertEqual(updated_thread.votes, -1)
        self.assertTrue(updated_thread.has_downvoted(self.user))

    def test_thread_vote_removal(self):
        # Upvote the thread
        self.thread.up_vote(self.user)
        # Retrieve the updated thread from the database
        updated_thread = Thread.objects.get(id=self.thread.id)
        self.assertEqual(updated_thread.votes, 1)
        self.assertTrue(updated_thread.has_upvoted(self.user))
        # Upvote the thread again (should remove the vote)
        self.thread.up_vote(self.user)
        # Retrieve the updated thread from the database
        updated_thread = Thread.objects.get(id=self.thread.id)
        self.assertEqual(updated_thread.votes, 0)
        self.assertFalse(updated_thread.has_upvoted(self.user))

class CommentModelTest(TestCase):
    def setUp(self):
        # Create a user
        self.user = User.objects.create(username='testuser', password='Pass123Word!')
        # Create a thread
        self.thread = Thread.objects.create(title='Test Thread', content='Test Content', author=self.user)
        # Create a comment
        self.comment = Comment.objects.create(thread=self.thread, author=self.user, body='Test Comment')

    def test_comment_creation(self):
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(self.comment.thread, self.thread)
        self.assertEqual(self.comment.author, self.user)
        self.assertEqual(self.comment.body, 'Test Comment')
        self.assertEqual(self.comment.votes, 0)

    def test_comment_up_vote(self):
        # Upvote the comment
        self.comment.up_vote(self.user)
        # Retrieve the updated comment from the database
        updated_comment = Comment.objects.get(id=self.comment.id)
        self.assertEqual(updated_comment.votes, 1)
        self.assertTrue(updated_comment.has_upvoted(self.user))

    def test_comment_down_vote(self):
        # Downvote the comment
        self.comment.down_vote(self.user)
        # Retrieve the updated comment from the database
        updated_comment = Comment.objects.get(id=self.comment.id)
        self.assertEqual(updated_comment.votes, -1)
        self.assertTrue(updated_comment.has_downvoted(self.user))

    def test_comment_vote_removal(self):
        # Upvote the comment
        self.comment.up_vote(self.user)
        # Retrieve the updated comment from the database
        updated_comment = Comment.objects.get(id=self.comment.id)
        self.assertEqual(updated_comment.votes, 1)
        self.assertTrue(updated_comment.has_upvoted(self.user))
        # Upvote the comment again (should remove the vote)
        self.comment.up_vote(self.user)
        # Retrieve the updated comment from the database
        updated_comment = Comment.objects.get(id=self.comment.id)
        self.assertEqual(updated_comment.votes, 0)
        self.assertFalse(updated_comment.has_upvoted(self.user))