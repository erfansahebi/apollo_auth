# syntax = docker/dockerfile:1.2

FROM python:3.10-slim-buster

WORKDIR /app

RUN apt-get update
RUN pip install --upgrade pip pip-tools
RUN --mount=type=cache,target=/var/cache/apt \
    apt-get update && \
    apt-get install --no-install-recommends -y \
    curl git netcat build-essential autoconf automake libtool pkg-config libc++-dev libffi-dev
COPY requirements.txt /app/requirements.txt
RUN --mount=type=cache,target=/root/.cache \
    cd /app && \
    pip install --no-cache-dir -r requirements.txt
COPY . /app
RUN chmod +x /app/run.sh
EXPOSE 8000