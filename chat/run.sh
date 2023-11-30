#/bin/bash

echo "Bringing down any existing container..."
(docker stop browserlab-chat && docker container rm browserlab-chat) || echo "No container to stop"

echo "Bring up the container..."
docker run \
    -d \
    --rm \
    --gpus all \
    -v $(pwd)/client:/app/client \
    -v $(pwd)/server:/app/server \
    -v $(pwd)/huggingface-cache:/root/.cache/huggingface \
    -p 8003:8003 \
    --env HF_TOKEN=$(cat token) \
    --name browserlab-chat \
    --net=host \
    browserlab-chat

# Separately, serve the static client files
# that are in ./client
echo "Serving client files..."
docker exec \
    -d \
    browserlab-chat \
    python3 -m http.server -d /app/client --bind 0.0.0.0 8004

echo "Tailing logs..."
docker logs -f browserlab-chat
