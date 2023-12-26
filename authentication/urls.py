from django.urls import path
from . import views


urlpatterns = [
    path('profile/<str:user>', views.UserProfile.as_view(), name='profile'),
]