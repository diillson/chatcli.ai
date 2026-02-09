FROM debian:bookworm-slim

RUN apt-get update \
  && apt-get install -y --no-install-recommends \
    bash \
    ca-certificates \
    curl \
    git \
    gzip \
    tar \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . /app
