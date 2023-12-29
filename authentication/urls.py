from django.urls import path
from . import views


urlpatterns = [
    path('profile/<str:username>/', views.UserProfile.as_view(), name='user_profile'),
]