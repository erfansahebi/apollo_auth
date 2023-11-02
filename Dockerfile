# syntax = docker/dockerfile:1.2

FROM python:3.10-slim-buster as base
RUN apt-get update
RUN apt-get install --no-install-recommends -y curl git netcat
RUN pip install --upgrade pip pip-tools
RUN mkdir /app

FROM base as builder
RUN rm -f /etc/apt/apt.conf.d/docker-clean
RUN --mount=type=cache,target=/var/cache/apt \
    apt-get update && \
    apt-get install --yes --no-install-recommends \
    build-essential autoconf automake libtool pkg-config libc++-dev git libffi-dev
COPY requirements.txt /app/requirements.txt
RUN --mount=type=cache,target=/root/.cache \
    cd /app && \
    pip install --no-cache-dir -r requirements.txt

FROM base
COPY --from=builder /usr/local /usr/local
COPY . /app
RUN chmod +x /app/run.sh
WORKDIR /app
EXPOSE 8000