from django.urls import path
from .views import album_release

urlpatterns = [
    path('', album_release, name='album-release'),
]