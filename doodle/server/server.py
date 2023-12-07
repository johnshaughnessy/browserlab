import pipeline_sd14 as sd14
import pipeline_pixelart as pixelart
from flask import Flask, request, send_from_directory, jsonify
from PIL import Image
import torch
import base64
import os
import io

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

doodle_settings = {
    "prompt": "",
    "strength": 1.75,
    "guidance_scale": 5,
    "use_pixelart": False
}
pipe = None

STYLE_SD14 = 1
STYLE_PIXELART = 2
STYLE_FAST_SDXL = 3

@app.route('/doodle/settings', methods=['POST'])
def set_doodle_settings():
    global doodle_settings
    global pipe

    data = request.json

    if data["use_pixelart"] != doodle_settings["use_pixelart"]:
        if doodle_settings["use_pixelart"]:
            if pipe is not None:
                pixelart.delete(pipe)
            pipe = sd14.init()
        else:
            if pipe is not None:
                sd14.delete(pipe)
            pipe = pixelart.init()

    doodle_settings.update(data)
    return jsonify(doodle_settings)


@app.route('/doodle/image', methods=['POST'])
def get_image():
    global pipe
    global doodle_settings

    image_data = request.data.decode('utf-8')
    image_data = image_data.split('data:image/png;base64,')[1]
    image_data = base64.b64decode(image_data)
    init_image = Image.open(io.BytesIO(image_data)).convert('RGB')

    image = None;
    if doodle_settings["use_pixelart"]:
        if pipe is None:
            pipe = pixelart.init()
        image = pixelart.img2img(pipe, doodle_settings["prompt"], init_image, doodle_settings["strength"], doodle_settings["guidance_scale"])
    else:
        if pipe is None:
            pipe = sd14.init()
        image = sd14.img2img(pipe, doodle_settings["prompt"], init_image, doodle_settings["strength"], doodle_settings["guidance_scale"])

    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()

    response = app.response_class(img_byte_arr, mimetype='image/png')
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
