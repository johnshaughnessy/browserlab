import eventlet
import socketio
import json
import torch

from transformers import pipeline, set_seed
generator = pipeline('text-generation', model='gpt2')
set_seed(42)

def generate(prompt):

    print("\n\n\nPrompt: " + prompt)

    responses = generator(prompt, max_length=500, num_return_sequences=1)

    response = responses[0]['generated_text']
    print("\n\n\nFull response: " + response)

    # Do not include the prompt in the reply, but first check that the response is long enough
    if len(response) > len(prompt):
        response = response[len(prompt):]

    # print("\n\n\nResponse without prompt: " + response)

    stripped_response = strip_down_reply(response)

    print("\n\n\nStripped response: " + stripped_response)

    return stripped_response + "\n\n"

sio = socketio.Server()
app = socketio.WSGIApp(sio, static_files={'/': './client/dist/'})

@sio.event
def connect(sid, environ):
    print('connect ', sid)


prompt = [];
# Push onto prompt
prompt.append("The following is a conversation with an AI assistant. The assistant is helpful, creative, clever, and very friendly.\n\n");
prompt.append("USER: Hello, who are you?\n\n");
prompt.append("AI: I am an AI assistant ready to help you with anything you need. How can I help you today?\n\n");

def strip_down_reply(text):
    # Remove everything after "USER:", if it exists
    user_index = text.find("USER:")
    if user_index != -1:
        text = text[:user_index]
    # Remove newlines
    text = text.replace("\n", " ")
    return text


@sio.event
def message(sid, data):
    # Decode the JSON and reply
    message = json.loads(data)
    text = message.get('text')
    print("Received: " + text)
    prompt.append("USER: " + text + "\n\n")
    text_prompt = ''.join(prompt) + "AI:"
    aireply = generate(text_prompt);
    reply = {'text': aireply, 'isNewMessage': True }
    prompt.append("AI: " + aireply)
    print("Reply: " + json.dumps(reply))
    sio.emit('message', json.dumps(reply), room=sid)

@sio.event
def disconnect(sid):
    print('disconnect ', sid)

if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('', 8006)), app)
