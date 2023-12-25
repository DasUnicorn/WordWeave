from . import views
from django.urls import path

urlpatterns = [
    path('', views.GlobalTimeline.as_view(), name='home'),
]