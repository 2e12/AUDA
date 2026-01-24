from django.urls import path

from . import views

urlpatterns = [
    path("stream/<int:track_id>/", views.stream_audio, name="stream"),
]