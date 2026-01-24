from rest_framework import serializers, viewsets
from rest_framework import filters

from library.models import Playlist

from django_filters.rest_framework import DjangoFilterBackend

# Serializers define the API representation.
class PlaylistModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Playlist
        fields = ['id', 'name']

class PlaylistSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()


# ViewSets define the view behavior.
class PlaylistViewSet(viewsets.ModelViewSet):
    queryset = Playlist.objects.all()
    serializer_class = PlaylistModelSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["name"]
