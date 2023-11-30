import eventlet
import socketio
import json

sio = socketio.Server()
app = socketio.WSGIApp(sio, static_files={'/': 'client/dist/'})

@sio.event
def connect(sid, environ):
    print('connect ', sid)

@sio.event
def message(sid, data):
    # Decode the JSON and reply
    message = json.loads(data)
    print('message text', message.get('text'))
    reply = {'text': 'echo from server: ' + message.get('text') }
    sio.emit('message', json.dumps(reply), room=sid)

@sio.event
def disconnect(sid):
    print('disconnect ', sid)

if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('', 8005)), app)
