from django.urls import path
from . import views


urlpatterns = [
    path('profile/<slug:username>/', views.UserProfileView.as_view(), name='user_profile'),
]