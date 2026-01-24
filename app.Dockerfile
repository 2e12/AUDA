FROM python:3.13.9 AS builder

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1 

COPY app/requirements.txt /app/requirements.txt

RUN pip install --upgrade pip 
RUN pip install -r /app/requirements.txt
RUN pip install --no-cache-dir gunicorn

FROM python:3.13.9-slim

RUN apt update
RUN apt install --yes --no-install-recommends curl
RUN apt install --yes --no-install-recommends ffmpeg

RUN useradd -m -r appuser && \
   mkdir /app && \
   chown -R appuser /app
 
COPY --from=builder /usr/local/lib/python3.13/site-packages/ /usr/local/lib/python3.13/site-packages/
COPY --from=builder /usr/local/bin/ /usr/local/bin/

WORKDIR /app

COPY --chown=appuser:appuser app/ /app/
RUN chmod +x /app/entrypoint.sh

USER appuser

EXPOSE 8888
ENTRYPOINT ["/app/entrypoint.sh"]