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
from django.shortcuts import get_object_or_404, redirect, reverse
from django.core.paginator import Paginator, EmptyPage

# Create your views here.


class GlobalTimeline(generic.ListView):
    paginate_by = 5
    queryset = Thread.objects.all()
    template_name = "index.html"


class UserTimelineView(LoginRequiredMixin, generic.ListView):
    paginate_by = 5
    template_name = "timeline.html"
    context_object_name = 'tag_timeline'
    login_url = '/accounts/login/'

    def get_queryset(self):
        user = self.request.user
        followed_tags = Tag.objects.filter(following__followed_by=user)
        followed_threads = Thread.objects.filter(tags__in=followed_tags).distinct()

        return followed_threads

class InfoView(TemplateView):
    template_name = "info.html"

#  LoginRequiredMixin is used to ensure that only logged-in users can create threads.
class CreateThreadView(LoginRequiredMixin, FormView):
    template_name = 'create_thread.html'
    form_class = ThreadForm
    success_url = reverse_lazy('home')  # Redirect to a view that displays a list of threads

    def form_valid(self, form):
        # Set the author before saving the form
        form.instance.author = self.request.user
        form.save()
        return super().form_valid(form)

class TagSiteView(generic.ListView):
    template_name = "tag_site.html"
    context_object_name = 'thread_list'

    def get_queryset(self):
        tag_slug = self.kwargs['slug']
        return Thread.objects.filter(tags__slug=tag_slug)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag_slug = self.kwargs['slug']

        tag = get_object_or_404(Tag, slug=tag_slug)
        context['tag'] = tag

        user_follows_tag = False
        if self.request.user.is_authenticated:
            user_follows_tag = Follower.objects.filter(followed_by=self.request.user, following=tag).exists()

        context['user_follows_tag'] = user_follows_tag

        return context


class ThreadDetailView(DetailView):
    model = Thread
    template_name = 'thread_detail.html'
    context_object_name = 'thread'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        context['comments'] = self.object.comments.all()  # Retrieve comments for the thread
        return context

class AddCommentView(View):
    def post(self, request, thread_id):
        thread = Thread.objects.get(id=thread_id)
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.thread = thread
            comment.author = request.user
            comment.save()

        return redirect('thread_detail', thread_id=thread.id, slug=thread.slug)

class MyPaginator(Paginator):
    def validate_number(self, number):
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
    thread = get_object_or_404(Thread, pk=thread_id) # pk lookup shortcut, which stands for “primary key”.
    thread.up_vote(request.user)
    return redirect('home')

@require_POST
@login_required
def downvote_thread(request, thread_id):
    thread = get_object_or_404(Thread, pk=thread_id) # pk lookup shortcut, which stands for “primary key”.
    thread.down_vote(request.user)
    return redirect('home')

@require_POST
@login_required
def upvote_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id) # pk lookup shortcut, which stands for “primary key”.
    comment.up_vote(request.user)
    thread = get_object_or_404(Thread, pk=comment.thread.id)
    return redirect('thread_detail', thread_id=thread.id, slug=thread.slug)

@require_POST
@login_required
def downvote_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id) # pk lookup shortcut, which stands for “primary key”.
    comment.down_vote(request.user)
    thread = get_object_or_404(Thread, pk=comment.thread.id)
    return redirect('thread_detail', thread_id=thread.id, slug=thread.slug)

@login_required
def edit_thread(request, thread_id):
    thread = get_object_or_404(Thread, id=thread_id, author=request.user)

    if request.method == 'POST':
        form = ThreadForm(request.POST, instance=thread)
        if form.is_valid():
            form.save()
            return redirect('thread_detail', thread_id=thread.id, slug=thread.slug)
    else:
        form = ThreadForm(instance=thread)

    return render(request, 'edit_thread.html', {'form': form, 'thread': thread})

@login_required
def delete_thread(request, thread_id):
    thread = get_object_or_404(Thread, id=thread_id, author=request.user)

    if request.method == 'POST':
        # Handle the deletion of the thread
        thread.delete()
        return redirect('home') 

    # Render the delete confirmation page
    return render(request, 'delete_thread_confirm.html', {'thread': thread})

@login_required
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, author=request.user)

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('thread_detail', thread_id=comment.thread.id, slug=comment.thread.slug)
    else:
        form = CommentForm(instance=comment)

    return render(request, 'edit_comment.html', {'form': form, 'comment': comment})

@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, author=request.user)

    if request.method == 'POST':
        # Handle the deletion of the thread
        comment.delete()
        return redirect('thread_detail', thread_id=comment.thread.id, slug=comment.thread.slug)

    # Render the delete confirmation page
    return render(request, 'delete_comment_confirm.html', {'comment': comment})