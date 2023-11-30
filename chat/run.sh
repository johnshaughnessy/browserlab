#/bin/bash

(docker stop browserlab-chat && docker container rm browserlab-chat) || echo "No container to stop"

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
    browserlab-chat

docker logs -f browserlab-chat
