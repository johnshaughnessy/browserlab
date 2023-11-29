# Doodle

Video demos:

- https://www.youtube.com/watch?v=3y3eY9DFZMQ
- https://www.youtube.com/watch?v=QH9Zqv0iC6I

## Client

Browser. Javascript. HTML.

A text input where the user can write a prompt.
A canvas where the user can draw.
A canvas where the AI is generating images based on the two inputs.

## Server

Python

An api that accepts text and image, runs diffusion inference, and returns an image.

## Setup

0. Get an hugging face access token from https://huggingface.co/settings/tokens so that you can download the model. Save it as a file called `token` in this directory
1. Run `./init.sh` to build the docker image.
1. Run `./run.sh` to run the docker image.
1. Open `http://localhost:8001` in your browser.

The first time you run the app, the server will download the model.
The `./run.sh` command will mount `client/` and `server/` directories, so you can easily edit the code to play around with while the container keeps running.
