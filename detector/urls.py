from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('video-feed/', views.video_feed, name='video_feed'),
    path('image-detection/', views.image_detection, name='image_detection'),
]
