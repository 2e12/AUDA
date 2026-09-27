import os

from uuid import uuid4
from json import loads

from django.http import Http404
from rest_framework import serializers, viewsets
from rest_framework.response import Response
from rest_framework import filters
from rest_framework.decorators import action

from django_filters.rest_framework import DjangoFilterBackend

from library.models import Track, Playlist

from api.playlist import PlaylistSerializer

from pydub import AudioSegment
from pydub.utils import mediainfo

from pytubefix import YouTube
from pytubefix import Playlist as YPlaylist
from pytubefix.cli import on_progress


class TrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Track
        fields = ['id', 'name', 'artist', 'file', 'playlists']

class YoutubeTrackSerializer(serializers.Serializer):
    youtube_link = serializers.URLField()
    name = serializers.CharField(allow_blank=True)
    artist = serializers.CharField(allow_blank=True)
    playlists = serializers.ListField(child=serializers.IntegerField(), allow_empty=True)

class TrackSliceSeralizer(serializers.Serializer):
    name = serializers.CharField()
    artist = serializers.CharField()
    range = serializers.ListField(child=serializers.IntegerField(), allow_empty=False, min_length=2, max_length=2)

class SlicesSeralizer(serializers.Serializer):
    slices = serializers.ListSerializer(child=TrackSliceSeralizer())
    playlists = serializers.ListField(child=serializers.IntegerField(), allow_empty=True)



class TrackViewSet(viewsets.ModelViewSet):
    queryset = Track.objects.all()
    serializer_class = TrackSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['name', 'file', 'artist']
    filterset_fields = ["playlists"]

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            if os.path.exists(instance.filename):
                os.remove(instance.filename)
            self.perform_destroy(instance)
        except Http404:
            pass
        return Response(status=204)
    
    @action(detail=True, methods=['POST'])
    def create_slices(self, request, pk):
        initalAudio = self.get_object()
        initalAudioFile = AudioSegment.from_file(initalAudio.filename)
        task = SlicesSeralizer(data=request.data)
        tracks = []
        if not task.is_valid():
            return Response(status=400)
        for slice in task.data["slices"]:
            filename = f"{uuid4().hex}.ogg"
            folder = "media"
            initalAudioFile[slice["range"][0]*1000:slice["range"][1]*1000].fade_in(1000).fade_out(1000).export(f"{folder}/{filename}", format="ogg", bitrate="128k")
            track = Track(filename=f"{folder}/{filename}", name=slice["name"], file=f"{folder}/{filename}", artist=slice["artist"])
            track.save()
            tracks.append(track)
        for track in tracks:
            for playlist_id in task.data["playlists"]:
                track.playlists.add(Playlist.objects.get(pk=playlist_id))
                track.save()
        return Response(TrackSerializer(tracks, many=True).data, status=201)

    @action(detail=False, methods=['POST'])
    def fetch_youtube_playlist(self, request):
        pl = YPlaylist(request.data["youtube_playlist_link"])
        videos = []
        for video in pl.videos:
            videos.append({
                'name': video.title,
                'artist': video.author,
                'url': video.watch_url
            })
        return Response({'videos': videos, 'playlist_name': pl.title}, status=200)
    
    @action(detail=True, methods=['GET'])
    def show_playlists(self, request, pk):
        playlists = Playlist.objects.filter(tracks__in=[pk])
        playlists = PlaylistSerializer(playlists, many=True)
        return Response(playlists.data, status=200)

    @action(detail=False, methods=['POST'])
    def load_youtube_video(self, request):
        trackreq = YoutubeTrackSerializer(data=request.data)
        if not trackreq.is_valid():
            return Response(status=400)
        
        filename = f"{uuid4().hex}.ogg"
        folder = "media"

        yt = YouTube(trackreq.data["youtube_link"], on_progress_callback = on_progress, client="WEB")
        ys = yt.streams.get_audio_only()
        ys.download(filename=f"{filename}.tmp", output_path=folder)
        
        if trackreq.data["name"] == "":
            name = yt.title
        else:
            name = trackreq.data["name"]

        if trackreq.data["artist"] == "":
            artist = yt.author
        else:
            artist = trackreq.data["artist"]

        sound = AudioSegment.from_file(f"{folder}/{filename}.tmp", "mp4")
        sound.export(f"{folder}/{filename}", format="ogg", bitrate="128k")
        os.remove(f"{folder}/{filename}.tmp")
        track = Track(filename=f"{folder}/{filename}", name=name, file=f"{folder}/{filename}", artist=artist)
        track.save()
        for playlist_id in trackreq.data["playlists"]:
            track.playlists.add(Playlist.objects.get(pk=playlist_id))
        track.save()
        return Response({'id': track.id}, status=201)

    @action(detail=False, methods=['POST'])
    def upload_file(self, request):
        name = ""
        playlists = []
        trackreq = TrackSerializer(data=request.data)
        if not trackreq.is_valid():
            return Response(status=400)
        name = trackreq.data["name"]
        sound = AudioSegment.from_file_using_temporary_files(request.data['file'])
        filename = f"{uuid4().hex}.ogg"
        folder = "media"
        sound.export(f"{folder}/{filename}", format="ogg", bitrate="128k")
        if name == "":
            name = request.data["file"].name
        track = Track(filename=f"{folder}/{filename}", name=name, file=f"{folder}/{filename}", artist=trackreq.data["artist"])
        track.save()
        for playlist_id in playlists:
            track.playlists.add(Playlist.objects.get(pk=playlist_id))
        track.save()
        return Response({'id': track.id}, status=201)
    