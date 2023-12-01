from flask import Flask, request, send_from_directory, jsonify
import subprocess
import os

app = Flask(__name__, static_folder='../client')

# Save root browserlab directory, which is two levels up from server.py
browserlab_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
print(browserlab_root)

def init_app(app_name):
    print(f'init {app_name}')
    try:
        os.chdir(browserlab_root)
        os.chdir(app_name)
        # List files in the current directory
        print(os.listdir())
        subprocess.run(["./init.sh"], check=True)
        return {'status': 'success', 'message': f'{app_name} initialized'}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}

def run_app(app_name):
    print(f'run {app_name}')
    try:
        os.chdir(browserlab_root)
        os.chdir(app_name)
        subprocess.run(["./run.sh", "&"], shell=True) # '&' to run in background
        return {'status': 'success', 'message': f'{app_name} started'}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}

def stop_app(app_name):
    print(f'stop {app_name}')
    try:
        os.chdir(browserlab_root)
        os.chdir(app_name)
        subprocess.run(["docker", "container", "stop", f"browserlab-{app_name}"])
        return {'status': 'success', 'message': f'{app_name} stopped'}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}

#
#  {
#    "status": 'success' | 'error',
#    "doodle": "running" | "booting" | "stopped" | "error",
#    "chat": "running" | "booting" | "stopped" | "error",
#    "websocket": "running" | "booting" | "stopped" | "error",
#  }
def container_status():
    try:
        os.chdir(browserlab_root)
        subprocess.run(["docker", "ps"])
        is_doodle_running = subprocess.run(["docker", "ps", "-q", "-f", "name=browserlab-doodle"], stdout=subprocess.PIPE).stdout.decode('utf-8')
        is_websocket_running = subprocess.run(["docker", "ps", "-q", "-f", "name=browserlab-websocket"], stdout=subprocess.PIPE).stdout.decode('utf-8')
        is_chat_running = subprocess.run(["docker", "ps", "-q", "-f", "name=browserlab-chat"], stdout=subprocess.PIPE).stdout.decode('utf-8')
        # TODO: Handle booting and error states for each container
        return {
            'status': 'success',
            'doodle': 'running' if is_doodle_running else 'stopped',
            'websocket': 'running' if is_websocket_running else 'stopped',
            'chat': 'running' if is_chat_running else 'stopped',
        }
    except Exception as e:
        return {'status': 'error', 'message': str(e)}

@app.route('/api/status', methods=['GET'])
def status():
    return container_status()

@app.route('/api/doodle/init', methods=['POST'])
def doodle_init():
    return init_app('doodle')

@app.route('/api/doodle/run', methods=['POST'])
def doodle_run():
    return run_app('doodle')

@app.route('/api/doodle/stop', methods=['POST'])
def doodle_stop():
    return stop_app('doodle')

@app.route('/api/websocket/init', methods=['POST'])
def websocket_init():
    return init_app('websocket')

@app.route('/api/websocket/run', methods=['POST'])
def websocket_run():
    return run_app('websocket')

@app.route('/api/websocket/stop', methods=['POST'])
def websocket_stop():
    return stop_app('websocket')

@app.route('/api/chat/init', methods=['POST'])
def chat_init():
    return init_app('chat')

@app.route('/api/chat/run', methods=['POST'])
def chat_run():
    return run_app('chat')

@app.route('/api/chat/stop', methods=['POST'])
def chat_stop():
    return stop_app('chat')

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_client(path):
    if path != "" and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8002)
