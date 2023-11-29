#/bin/bash

(docker stop browserlab-doodle && docker container rm browserlab-doodle) || echo "No container to stop"

docker run \
    -d \
    --rm \
    --gpus all \
    -v $(pwd)/client:/app/client \
    -v $(pwd)/server:/app/server \
    -v $(pwd)/huggingface-cache:/root/.cache/huggingface \
    -p 8001:8001 \
    --env HF_TOKEN=$(cat token) \
    --name browserlab-doodle \
    browserlab-doodle

docker logs -f browserlab-doodle
