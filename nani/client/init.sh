#!/bin/bash
echo "Installing client dependencies."

rm -f dist/*
docker build -f Dockerfile.nani-client -t browserlab-nani-client .
docker run -it --rm \
    --name browserlab-nani-client \
    -v "$PWD":/app \
    -w /app \
    browserlab-nani-client \
    npm run build
