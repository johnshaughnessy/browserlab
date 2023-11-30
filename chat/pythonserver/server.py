from flask import Flask, request, send_from_directory, jsonify
from flask_sockets import Sockets
import os
import json
import logging

app = Flask(__name__, static_folder='../client')
sockets = Sockets(app)
logging.basicConfig(level=logging.DEBUG)
app.logger.setLevel(logging.DEBUG)

@sockets.route('/chat')
def handle_message(message):
    logging.debug("Received a chat message from the client!")
    logging.debug(message)
    # Send the chat message to all clients
    # The message is json, so we need to parse it first
    message = json.loads(message)
    # Then we can send it to all clients


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_client(path):
    if path != "" and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

if __name__ == "__main__":
    # Run the app with flask_sockets
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler
    server = pywsgi.WSGIServer(('', 8003), app, handler_class=WebSocketHandler)
    server.serve_forever()
