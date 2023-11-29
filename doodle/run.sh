#!/bin/bash
docker run \
    -d \
    -v $(pwd)/client:/app/client \
    -v $(pwd)/server:/app/server \
    -p 8001:8001 \
    browserlab-doodle

# Open firefox to http://localhost:8001
# Use a flag to open it in a new window
firefox -new-window http://localhost:8001
