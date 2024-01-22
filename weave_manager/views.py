from django.views import generic
from .models import Thread, Comment
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView
from django.views.generic.edit import FormView
from .forms import ThreadForm
from django.urls import reverse_lazy
from .forms import CommentForm
from django.views import View
from django.shortcuts import get_object_or_404, redirect

# Create your views here.


class GlobalTimeline(generic.ListView):
    queryset = Thread.objects.all()
    template_name = "index.html"

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
    def post(self, request, slug):
        thread = Thread.objects.get(slug=slug)
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.thread = thread
            comment.author = request.user
            comment.save()

        return redirect('thread_detail', slug=slug)

def upvote_thread(request, thread_id):
    thread = get_object_or_404(Thread, pk=thread_id) # pk lookup shortcut, which stands for “primary key”.
    thread.up_vote(request.user)
    return redirect('home')

def downvote_thread(request, thread_id):
    thread = get_object_or_404(Thread, pk=thread_id) # pk lookup shortcut, which stands for “primary key”.
    thread.down_vote(request.user)
    return redirect('home')

def upvote_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id) # pk lookup shortcut, which stands for “primary key”.
    comment.up_vote(request.user)
    thread = get_object_or_404(Thread, pk=comment.thread.id)
    return redirect('thread_detail', slug=thread.slug)

def downvote_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id) # pk lookup shortcut, which stands for “primary key”.
    comment.down_vote(request.user)
    thread = get_object_or_404(Thread, pk=comment.thread.id)
    return redirect('thread_detail', slug=thread.slug)