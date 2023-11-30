echo "Installing client dependencies."

docker run -it --rm \
    --name browserlab-chat \
    -v "$PWD"/client:/app/client \
    -w /app/client \
    node:18 \
    npm ci

echo "Building the client."

docker run -it --rm \
    --name browserlab-chat \
    -v "$PWD"/client:/app/client \
    -w /app/client \
    node:18 \
    npm run build

echo "Building the server."

docker build -f Dockerfile.chat-server -t browserlab-chat-server .
