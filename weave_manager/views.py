from django.views import generic
from .models import Thread, Comment
from follow.models import Follower
from taggit.models import Tag
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, TemplateView
from django.views.generic.edit import FormView
from .forms import ThreadForm
from django.urls import reverse_lazy
from .forms import CommentForm
from django.views import View
from django.shortcuts import get_object_or_404, redirect  # noqa: F811
from django.core.paginator import Paginator, EmptyPage
from django.contrib import messages


class GlobalTimeline(generic.ListView):
    """
    Global Timeline that displays all threads.
    This view has pagination.
    """
    paginate_by = 5
    queryset = Thread.objects.all()
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        """returns a list of all threads"""
        context = super().get_context_data(**kwargs)
        thread_list = context['thread_list']
        if self.request.user.is_authenticated:
            for thread in thread_list:
                thread.has_upvoted = thread.has_upvoted(self.request.user)
                thread.has_downvoted = thread.has_downvoted(self.request.user)
        return context


class UserTimelineView(LoginRequiredMixin, generic.ListView):
    """
    Timeline containing all threads with tags
    the logged in user is following.
    """
    paginate_by = 5
    template_name = "timeline.html"
    context_object_name = 'tag_timeline'
    login_url = '/accounts/login/'

    def get_queryset(self):
        """returns a list of threads with tags a user is following."""
        user = self.request.user
        followed_tags = Tag.objects.filter(following__followed_by=user)
        followed_threads = Thread.objects.filter(
            tags__in=followed_tags).distinct()

        return followed_threads

    def get_context_data(self, **kwargs):
        """Returns the vote info for the user on each thread."""
        context = super().get_context_data(**kwargs)
        thread_list = context['tag_timeline']
        if self.request.user.is_authenticated:
            for thread in thread_list:
                thread.has_upvoted = thread.has_upvoted(self.request.user)
                thread.has_downvoted = thread.has_downvoted(self.request.user)
        return context


class InfoView(TemplateView):
    """Sets Info View template."""
    template_name = "info.html"


# LoginRequiredMixin is used to ensure that only logged-in users
# can create threads.
class CreateThreadView(LoginRequiredMixin, FormView):
    """
    View to create a new thread.
    Logged in User required.
    """
    template_name = 'create_thread.html'
    form_class = ThreadForm
    # Redirect to a view that displays a list of threads
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        """Validate form data. Sends message on success."""
        # Set the author before saving the form
        form.instance.author = self.request.user
        form.save()
        messages.add_message(self.request, messages.INFO,
                             'Your Thread has been created.')
        return super().form_valid(form)


class TagSiteView(generic.ListView):
    """
    View to surply data for the tagsite.
    """
    template_name = "tag_site.html"
    context_object_name = 'thread_list'

    def get_queryset(self):
        """returns slug of a thread"""
        tag_slug = self.kwargs['slug']
        return Thread.objects.filter(tags__slug=tag_slug)

    def get_context_data(self, **kwargs):
        """
        Returns the info if a user is following a given tag,
        as well as the information if the user has up or downvoted a thread.
        """
        context = super().get_context_data(**kwargs)
        tag_slug = self.kwargs['slug']

        tag = get_object_or_404(Tag, slug=tag_slug)
        context['tag'] = tag

        user_follows_tag = False
        if self.request.user.is_authenticated:
            user_follows_tag = Follower.objects.filter(
                followed_by=self.request.user, following=tag).exists()

        context['user_follows_tag'] = user_follows_tag

        thread_list = context['thread_list']
        if self.request.user.is_authenticated:
            for thread in thread_list:
                thread.has_upvoted = thread.has_upvoted(self.request.user)
                thread.has_downvoted = thread.has_downvoted(self.request.user)

        return context


class ThreadDetailView(DetailView):
    model = Thread
    template_name = 'thread_detail.html'
    context_object_name = 'thread'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        # Retrieve comments for the thread
        context['comments'] = self.object.comments.all()

        thread = context['thread']
        if self.request.user.is_authenticated:
            thread.has_upvoted = thread.has_upvoted(self.request.user)
            thread.has_downvoted = thread.has_downvoted(self.request.user)

        comment_list = context['comments']
        if self.request.user.is_authenticated:
            for comment in comment_list:
                comment.has_upvoted = comment.has_upvoted(self.request.user)
                comment.has_downvoted = comment.has_downvoted(
                    self.request.user)

        return context


class AddCommentView(View):
    """
    View for creating a comment.
    """
    def post(self, request, thread_id):
        """Post request handling, saves comment and returns to thread."""
        thread = Thread.objects.get(id=thread_id)
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.thread = thread
            comment.author = request.user
            comment.save()
            messages.add_message(self.request, messages.INFO,
                                 'Your Comment has been created.')

        return redirect('thread_detail', thread_id=thread.id, slug=thread.slug)


class MyPaginator(Paginator):
    """
    Pagination for site.

    Keyword Arguments:
    numer -- int, the maximum number of objects per page.
    """
    def validate_number(self, number):
        """Validate the number of objects per page"""
        try:
            return super().validate_number(number)
        except EmptyPage:
            if int(number) > 1:
                # return the last page
                return self.num_pages
            elif int(number) < 1:
                # return the first page
                return 1
            else:
                raise


@require_POST
@login_required
def upvote_thread(request, thread_id):
    """
    Upvote a given thread.
    User has to be logged in.

    Keyword Argument:
    thread_id -- the id of the thread that should get upvoted.
    """
    # pk lookup shortcut, which stands for “primary key”.
    thread = get_object_or_404(Thread, pk=thread_id)
    thread.up_vote(request.user)
    return redirect('home')


@require_POST
@login_required
def downvote_thread(request, thread_id):
    """
    Downvote a given thread.
    User has to be logged in.

    Keyword Argument:
    thread_id -- the id of the thread that should get downvoted.
    """
    # pk lookup shortcut, which stands for “primary key”.
    thread = get_object_or_404(Thread, pk=thread_id)
    thread.down_vote(request.user)
    return redirect('home')


@require_POST
@login_required
def upvote_comment(request, comment_id):
    """
    Upvote a given comment.
    User has to be logged in.

    Keyword Argument:
    comment_id -- the id of the comment that should get upvoted.
    """
    # pk lookup shortcut, which stands for “primary key”.
    comment = get_object_or_404(Comment, pk=comment_id)
    comment.up_vote(request.user)
    thread = get_object_or_404(Thread, pk=comment.thread.id)
    return redirect('thread_detail', thread_id=thread.id, slug=thread.slug)


@require_POST
@login_required
def downvote_comment(request, comment_id):
    """
    Downvote a given comment.
    User has to be logged in.

    Keyword Argument:
    comment_id -- the id of the comment that should get downvoted.
    """
    # pk lookup shortcut, which stands for “primary key”.
    comment = get_object_or_404(Comment, pk=comment_id)
    comment.down_vote(request.user)
    thread = get_object_or_404(Thread, pk=comment.thread.id)
    return redirect('thread_detail', thread_id=thread.id, slug=thread.slug)


@login_required
def edit_thread(request, thread_id):
    """
    Edit a given thread.
    User has to be logged in.

    Keyword Argument:
    thread_id -- the id of the thread that should get edited.
    """
    thread = get_object_or_404(Thread, id=thread_id, author=request.user)

    if request.method == 'POST':
        form = ThreadForm(request.POST, instance=thread)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.INFO,
                                 'Your Thread has been edited.')
            return redirect('thread_detail', thread_id=thread.id,
                            slug=thread.slug)
    else:
        form = ThreadForm(instance=thread)

    return render(request, 'edit_thread.html',
                  {'form': form, 'thread': thread})


@login_required
def delete_thread(request, thread_id):
    """
    Delete a given thread.
    User has to be logged in.

    Keyword Argument:
    thread_id -- the id of the thread that should get deteled.
    """
    thread = get_object_or_404(Thread, id=thread_id, author=request.user)

    if request.method == 'POST':
        # Handle the deletion of the thread
        messages.add_message(request, messages.INFO,
                             'Your Thread has been deleted.')
        thread.delete()
        return redirect('home')

    # Render the delete confirmation page
    return render(request, 'delete_thread_confirm.html', {'thread': thread})


@login_required
def edit_comment(request, comment_id):
    """
    Edit a given comment.
    User has to be logged in.

    Keyword Argument:
    comment_id -- the id of the comment that should get edited.
    """
    comment = get_object_or_404(Comment, id=comment_id, author=request.user)

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.INFO,
                                 'Your Comment has been edited.')
            return redirect('thread_detail', thread_id=comment.thread.id,
                            slug=comment.thread.slug)
    else:
        form = CommentForm(instance=comment)

    return render(request, 'edit_comment.html', {'form': form,
                                                 'comment': comment})


@login_required
def delete_comment(request, comment_id):
    """
    Delete a given comment.
    User has to be logged in.

    Keyword Argument:
    comment_id -- the id of the comment that should get delted.
    """
    comment = get_object_or_404(Comment, id=comment_id, author=request.user)

    if request.method == 'POST':
        # Handle the deletion of the thread
        messages.add_message(request, messages.INFO,
                             'Your Comment has been deleted.')
        comment.delete()
        return redirect('thread_detail', thread_id=comment.thread.id,
                        slug=comment.thread.slug)

    # Render the delete confirmation page
    return render(request, 'delete_comment_confirm.html', {'comment': comment})
