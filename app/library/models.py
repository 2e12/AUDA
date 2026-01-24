from django.db import models

class Playlist(models.Model):
    name = models.CharField(max_length=255, db_index=True)

    def __str__(self):
        return self.name

class Track(models.Model):
    name = models.CharField(max_length=255, db_index=True, blank=True)
    file = models.FileField(null=True, upload_to="media")
    artist = models.CharField(max_length=255, db_index=True, blank=True)
    filename = models.CharField(max_length=50)
    playlists = models.ManyToManyField(Playlist, related_name="tracks")

    def __str__(self):
        return self.name