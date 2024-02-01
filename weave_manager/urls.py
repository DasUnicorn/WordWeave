from . import views
from .views import CreateThreadView, TagSiteView, InfoView, AddCommentView, ThreadDetailView, upvote_thread, downvote_thread, upvote_comment, downvote_comment
from django.urls import path

urlpatterns = [
    path('', views.GlobalTimeline.as_view(), name='home'),
    path('create_thread', CreateThreadView.as_view(), name='create_thread'),
    path('upvote/<int:thread_id>/', upvote_thread, name='upvote_thread'),
    path('downvote/<int:thread_id>/', downvote_thread, name='downvote_thread'),
    path('upvote_comment/<int:comment_id>/', upvote_comment, name='upvote_comment'),
    path('downvote_comment/<int:comment_id>/', downvote_comment, name='downvote_comment'),
    path('thread/<slug:slug>/add_comment/', AddCommentView.as_view(), name='add_comment'),
    path('thread/<int:thread_id>/edit/', views.edit_thread, name='edit_thread'),
    path('thread/<int:thread_id>/delete/', views.delete_thread, name='delete_thread'),
    path('comment/<int:comment_id>/edit/', views.edit_comment, name='edit_comment'),
    path('comment/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),
    path('thread/<slug:slug>/', ThreadDetailView.as_view(), name='thread_detail'),
    path('tag/<slug:slug>/', TagSiteView.as_view(), name='tag_site'),
    path('info/', InfoView.as_view(), name='info'),
]