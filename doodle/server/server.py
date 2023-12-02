from doodle_diffusion import process_image_with_prompt, process_image_pixelart, init_pipeline, init_pipeline_pixelart
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
init_pipeline()
#init_pipeline_pixelart()

app = Flask(__name__, static_folder='../client')

# Global variables
doodle_settings = {
    "prompt": "",
    "strength": 1.75,
    "guidance_scale": 5,
    "use_pixelart": False
}

@app.route('/doodle/settings', methods=['POST'])
def set_doodle_settings():
    global doodle_settings
    data = request.json
    doodle_settings.update(data)
    print("Updated doodle settings:", doodle_settings)
    return jsonify(doodle_settings)


@app.route('/doodle/image', methods=['POST'])
def get_image():
    image_data = request.data.decode('utf-8')

     # Extracting the Base64 part and decoding
    if image_data.startswith('data:image/png;base64,'):
        image_data = image_data.split('data:image/png;base64,')[1]
        image_data = base64.b64decode(image_data)

    # Call the process_image_with_prompt function
    if False:
        print("Using pixelart!")
        processed_image_data = process_image_pixelart(image_data, doodle_settings["prompt"], doodle_settings["strength"], doodle_settings["guidance_scale"])
    else:
        print("Not using pixelart!")
        processed_image_data = process_image_with_prompt(image_data, doodle_settings["prompt"], doodle_settings["strength"], doodle_settings["guidance_scale"])

    # Return the processed image
    response = app.response_class(processed_image_data, mimetype='image/png')
    return response

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_client(path):
    if path != "" and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8001)
