#!/bin/bash
docker run -it --rm \
    --name browserlab-websocket \
    -v "$PWD"/server:/app/server \
    -v "$PWD"/client:/app/client \
    -w /app/ \
    -p 8005:8005 \
    browserlab-websocket \
    python3 server/server.py
