echo "Building the client."
docker run -it --rm \
    --name browserlab-chat \
    -v "$PWD"/client:/app/client \
    -w /app/client \
    node:18 \
    npm run build

echo "Running the server."
docker run -it --rm \
    --name browserlab-chat-server \
    --gpus all \
    -v "$PWD"/server:/app/server \
    -v "$PWD"/client:/app/client \
    -v "$PWD"/huggingface-cache:/root/.cache/huggingface \
    -w /app/ \
    -p 8006:8006 \
    browserlab-chat-server \
    python3 server/server.py
