from django.urls import path
from . import views


urlpatterns = [
    path('profile/<slug:username>/', views.UserProfile.as_view(), name='user_profile'),
]