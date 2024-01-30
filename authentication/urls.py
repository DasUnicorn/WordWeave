from django.urls import path
from . import views


urlpatterns = [
    path('profile/<int:user_id>/delete/', views.delete_profile, name='delete_profile'),
    path('profile/settings/', views.ProfileUpdateView.as_view(), name='update_profile'),
    path('profile/<slug:username>/', views.UserProfileView.as_view(), name='user_profile'),
]