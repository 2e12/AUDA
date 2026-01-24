from rest_framework import routers

from api.track import TrackViewSet
from api.playlist import PlaylistViewSet

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'tracks', TrackViewSet)
router.register(r'playlists', PlaylistViewSet)