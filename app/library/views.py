import os
import re
import mimetypes
from django.http import HttpResponseNotFound, HttpResponse, StreamingHttpResponse
from django.shortcuts import get_object_or_404

from library.models import Track

def stream_audio(request, track_id):
    track = get_object_or_404(Track, pk=track_id)
    if not os.path.exists(track.filename):
        return HttpResponseNotFound("Audio file not found")

    file_size = os.path.getsize(track.filename)
    range_header = request.headers.get("Range", "")
    range_match = re.match(r"bytes=(\d+)-(\d*)", range_header)    

    if range_match:
        start = int(range_match.group(1))
        end = range_match.group(2)
        end = int(end) if end else file_size - 1

        if start >= file_size or start > end:
            return HttpResponse(status=416)

        status_code = 206
    else:
        start = 0
        end = file_size - 1
        status_code = 200

    length = end - start + 1

    def file_iterator(file_path, offset, chunk_len, chunk_size=8192):
        with open(file_path, "rb") as f:
            f.seek(offset)
            bytes_left = chunk_len
            while bytes_left > 0:
                read_size = min(chunk_size, bytes_left)
                data = f.read(read_size)
                if not data:
                    break
                bytes_left -= len(data)
                yield data

    content_type, _ = mimetypes.guess_type(track.filename)
    content_type = content_type or "audio/ogg"

    response = StreamingHttpResponse(
        file_iterator(track.filename, start, length),
        status=status_code,
        content_type=content_type
    )

    response["Accept-Ranges"] = "bytes"
    response["Content-Length"] = str(length)

    if status_code == 206:
        response["Content-Range"] = f"bytes {start}-{end}/{file_size}"

    return response