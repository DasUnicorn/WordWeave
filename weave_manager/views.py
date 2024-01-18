from django.views import generic
from .models import Thread
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView
from django.views.generic.edit import FormView
from .forms import ThreadForm
from django.urls import reverse_lazy
from .forms import CommentForm
from django.views import View

# Create your views here.


class GlobalTimeline(generic.ListView):
    queryset = Thread.objects.all()
    template_name = "index.html"
    paginate_by = 6

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