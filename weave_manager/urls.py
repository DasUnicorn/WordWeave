from . import views
from .views import CreateThreadView, AddCommentView, ThreadDetailView
from django.urls import path

urlpatterns = [
    path('', views.GlobalTimeline.as_view(), name='home'),
    path('create_thread', CreateThreadView.as_view(), name='create_thread'),
    path('thread/<slug:slug>/add_comment/', AddCommentView.as_view(), name='add_comment'),
    path('thread/<slug:slug>/', ThreadDetailView.as_view(), name='thread_detail'),
]