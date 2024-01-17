from . import views
from .views import CreateThreadView
from .views import ThreadDetailView
from django.urls import path

urlpatterns = [
    path('', views.GlobalTimeline.as_view(), name='home'),
    path('create_thread', CreateThreadView.as_view(), name='create_thread'),
    path('thread/<slug:slug>/', ThreadDetailView.as_view(), name='thread_detail'),
]