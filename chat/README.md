# Chat

A simple GPU-accelerated chat interface.

## Setup

0. Put a hugging face access token into a file called `token` so that the server can download an LLM.
1. Run `./init.sh`.
2. Run `./run.sh`.
3. Open [http://localhost:8002](http://localhost:8002).

## Client

HTML, Javascript

Presents two scrollable text areas to the user.

The left text area is where they type.
When they press enter, their text is transferred to the right hand side and sent to the server.
The server's response is displayed below their text in the right hand side.

## Server

Python, Flask, HuggingFace Diffusers

A web server that accepts text, runs LLM inference, and returns text.
