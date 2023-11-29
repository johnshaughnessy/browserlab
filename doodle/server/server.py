from diffusers import StableDiffusionPipeline
from doodle_diffusion import process_image_with_prompt
from flask import Flask, request, send_from_directory, jsonify
import torch
import base64
import os

def check_cuda():
    print(f"CUDA version: {torch.version.cuda}")
    cuda_available = torch.cuda.is_available()
    print(f"CUDA available: {cuda_available}")
    if cuda_available:
        cuda_count = torch.cuda.device_count()
        print(f"Number of CUDA devices available: {cuda_count}")
        for i in range(cuda_count):
            print(f"CUDA Device {i}: {torch.cuda.get_device_name(i)}")
            print(f"Device name: {torch.cuda.get_device_name(0)}")

check_cuda()

app = Flask(__name__, static_folder='../client')

pipe = StableDiffusionPipeline.from_pretrained("CompVis/stable-diffusion-v1-4", use_auth_token=os.getenv('HF_TOKEN'))
pipe.to("cuda")

# Global variable to store the prompt
doodle_prompt = ""
doodle_strength = 1.75

@app.route('/doodle/strength', methods=['POST'])
def set_strength():
    global doodle_strength
    doodle_strength = request.data.decode('utf-8')
    print("We got strength:", doodle_strength)
    return jsonify({"strength": doodle_strength})

@app.route('/doodle/prompt', methods=['POST'])
def set_prompt():
    global doodle_prompt
    doodle_prompt = request.data.decode('utf-8')
    print("We got prompt:", doodle_prompt)
    return jsonify({"prompt": doodle_prompt})

# @app.route('/doodle/image', methods=['POST'])
# def get_image():
#     print("We received an image!")

#     response = app.response_class(image_data, mimetype='image/png')
#     return response


@app.route('/doodle/image', methods=['POST'])
def get_image():
    image_data = request.data.decode('utf-8')

     # Extracting the Base64 part and decoding
    if image_data.startswith('data:image/png;base64,'):
        image_data = image_data.split('data:image/png;base64,')[1]
        image_data = base64.b64decode(image_data)

    # Call the process_image_with_prompt function
    processed_image_data = process_image_with_prompt(pipe, image_data, doodle_prompt, doodle_strength)

    # Return the processed image
    response = app.response_class(processed_image_data, mimetype='image/png')
    return response

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_client(path):
    print("Hello, world!")


    print("loaded the model.")

    if path != "" and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8001)
