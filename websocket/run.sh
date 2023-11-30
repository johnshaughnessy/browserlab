docker run -it --rm \
    --name browserlab-websocket-server \
    -v "$PWD"/server:/app/server \
    -v "$PWD"/client:/app/client \
    -w /app/ \
    -p 8005:8005 \
    browserlab-websocket-server \
    python3 server/server.py
