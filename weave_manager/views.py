from django.shortcuts import render
from django.views import generic
from .models import Thread

# Create your views here.
class GlobalTimeline(generic.ListView):
    queryset = Thread.objects.all()
    template_name = "timeline/timeline.html"