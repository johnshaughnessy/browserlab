# Doodle

## Client

Browser. Javascript. HTML.

A text input where the user can write a prompt.
A canvas where the user can draw.
A canvas where the AI is generating images based on the two inputs.

## Server

Python

An api that accepts text and image, runs diffusion inference, and returns an image.

## Setup

Run `./init.sh` to build the docker image.
Run `./run.sh` to run the docker image, mounting the client and server directories, and opening `localhost:8001` in your browser.
