from .views import follow_tag, unfollow_tag, UserTagView
from django.urls import path

urlpatterns = [
    # ... your other URL patterns ...
    path('follow_tag/', follow_tag, name='follow_tag'),
    path('unfollow_tag/', unfollow_tag, name='unfollow_tag'),
    path('tags', UserTagView.as_view(), name='user_tags'),
]