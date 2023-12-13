import eventlet
import socketio
import json
import time
import torch
from transformers import ( AutoModelForCausalLM, AutoTokenizer, pipeline)
from peft import LoraConfig, PeftModel

sio = socketio.Server(cors_allowed_origins='*')
app = socketio.WSGIApp(sio, static_files={'/': './client/dist/'})
pipe = None

@sio.event
def connect(sid, environ):
    print('connect ', sid)

def init():
    global pipe
    model_name = "meta-llama/Llama-2-7b-chat-hf"
    device_map = {"": 0}
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        low_cpu_mem_usage=True,
        return_dict=True,
        torch_dtype=torch.float16,
        device_map=device_map,
    )
    tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
    tokenizer.pad_token = tokenizer.eos_token
    tokenizer.padding_side = "right"

    pipe = pipeline(task="text-generation", model=model, tokenizer=tokenizer, max_new_tokens=200)
    return pipe, model, tokenizer

init()

@sio.event
def message(sid, data):
    global pipe

    if pipe is None:
        # log warning and reply with error message
        print("Error: pipe is None")
        sio.emit('message', json.dumps("Error: pipe is None"), room=sid)
        return

    message = json.loads(data)
    text = message.get('text')
    focus = message.get('focus')
    context = message.get('context')

    if focus is None or context is None:
        print("Error: Received a message where focus or context is None")
        sio.emit('message', json.dumps("Error: Received a message where focus or context is None"), room=sid)
        return

    print("Received message: ", focus, context)

    prompt = f"Explain the following text in detail:\n\n```\n\n {focus} \n\n```\n\n The context in which the text appeared is:\n\n```\n\n{context}\n\n```\n\n Reply in 5 sentences or less. Be succinct without losing any important information. Do not reply with anything preamble like, \"Sure, here is a reply in 5 sentences or less.\" Just reply with the explanation ONLY."

    start_time = time.time()
    result = pipe(f"<s>[INST] {prompt} [/INST]")
    print("Time taken: ", time.time() - start_time)

    raw_reply = result[0]['generated_text']

    # The reply always starts with the prompt, so let's strip out everything before [/INST]:
    reply = raw_reply.split("[/INST]")[1]

    reply_message = { "reply" : reply }

    print("Sending reply: ", reply_message)
    sio.emit('message', json.dumps(reply_message), room=sid)

@sio.event
def disconnect(sid):
    print('disconnect ', sid)

if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('', 7007)), app)
