FROM python:3.8-slim-bookworm

ENV DEBIAN_FRONTEND=noninteractive
WORKDIR /app

# Copia o script versionado
COPY .devcontainer/start-vnc.sh /usr/local/bin/start-vnc.sh
RUN chmod +x /usr/local/bin/start-vnc.sh

# To linux ubuntu:
RUN apt-get update && apt-get install -y \
    chromium chromium-driver \
    xvfb fluxbox tigervnc-standalone-server tigervnc-common \
    procps \
    fonts-liberation libnss3 libxss1 libasound2 libatk-bridge2.0-0 libgtk-3-0 \
    libx11-6 libxcomposite1 libxcursor1 libxdamage1 libxrandr2 libgbm-dev \
    libglib2.0-0 libgconf-2-4 libfontconfig1 ca-certificates \
    curl wget unzip jq gnupg2 openssh-client git \
    && rm -rf /var/lib/apt/lists/*

ENV DISPLAY=:99
ENV VNC_PORT=5900

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY . /app

ENTRYPOINT ["/usr/local/bin/start-vnc.sh"]
