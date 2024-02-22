from . import views
from django.urls import path

urlpatterns = [
    path('', views.GlobalTimeline.as_view(), name='home'),
    path('create_thread', views.CreateThreadView.as_view(),
         name='create_thread'),
    path('upvote/<int:thread_id>/', views.upvote_thread, name='upvote_thread'),
    path('downvote/<int:thread_id>/',
         views.downvote_thread, name='downvote_thread'),
    path('upvote_comment/<int:comment_id>/',
         views.upvote_comment, name='upvote_comment'),
    path('downvote_comment/<int:comment_id>/',
         views.downvote_comment, name='downvote_comment'),
    path('thread/<int:thread_id>/add_comment/',
         views.AddCommentView.as_view(), name='add_comment'),
    path('thread/<int:thread_id>/edit/', views.EditThreadView.as_view(),
         name='edit_thread'),
    path('thread/<int:thread_id>/delete/',
         views.delete_thread, name='delete_thread'),
    path('comment/<int:comment_id>/edit/',
         views.edit_comment, name='edit_comment'),
    path('comment/<int:comment_id>/delete/',
         views.delete_comment, name='delete_comment'),
    path('thread/<int:thread_id>-<slug:slug>/',
         views.ThreadDetailView.as_view(), name='thread_detail'),
    path('tag/<slug:slug>/', views.TagSiteView.as_view(), name='tag_site'),
    path('info/', views.InfoView.as_view(), name='info'),
    path('timeline/', views.UserTimelineView.as_view(), name='timeline'),
]
