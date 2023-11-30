# Chat

GPU-accelerated chat interface.

## Client

HTML, Javascript

Presents two scrollable text areas to the user.

The left text area is where they type.
When they press enter, their text is transferred to the right hand side and sent to the server.
The server's response is displayed below their text in the right hand side.

## Server

Python, Flask, HuggingFace Diffusers

A web server that accepts text, runs LLM inference, and returns text.
