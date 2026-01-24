import os
import re

from django.http import HttpResponse
from django.http import HttpResponse, HttpResponseNotFound

from library.models import Track

def stream_audio(request, track_id):
    track = Track.objects.get(pk=track_id)
    if not os.path.exists(track.filename):
        return HttpResponseNotFound("Audio file not found")

    file_size = os.path.getsize(track.filename)
    range_header = request.headers.get("Range")

    match = re.match(r"bytes=(\d+)-(\d*)", range_header)
    if match:
        start = int(match.group(1))
        end = match.group(2)
        end = int(end) if end else file_size - 1
    else:
        start = 0
        end = file_size - 1

    length = end - start + 1

    with open(track.filename, "rb") as f:
        f.seek(start)
        data = f.read(length)

    response = HttpResponse(
        data,
        status=206,
        content_type="audio/mp3"
    )
    response["Content-Range"] = f"bytes {start}-{end}/{file_size}"
    response["Accept-Ranges"] = "bytes"
    response["Content-Length"] = str(length)
    return response
