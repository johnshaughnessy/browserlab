docker run -it --rm \
    --name browserlab-nani-server \
    --gpus all \
    -v "$PWD":/app \
    -v "$HOME"/.cache/huggingface:/root/.cache/huggingface \
    -w /app \
    -p 7007:7007 \
    browserlab-nani-server \
    python3 server.py
