import torch
from PIL import Image
import io
import os

def process_image_with_prompt(pipe, image_data, prompt, strength):
    """
    Process the given image and prompt using Stable Diffusion pipeline.

    :param pipe: Stable Diffusion pipeline.
    :param image_data: Byte data of the image.
    :param prompt: Text prompt for the Stable Diffusion model.
    :return: Processed image as byte data.
    """
    print("Processing the image...")

    # Convert byte data to PIL Image
    image = Image.open(io.BytesIO(image_data))

    print("Loaded the image! :D")

    # Process the image with the provided prompt
    processed_image = pipe(prompt=prompt, init_image=image, strength=strength).images[0]

    print("Processed the image! :D")

    # Convert PIL Image back to byte data
    img_byte_arr = io.BytesIO()
    processed_image.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()

    return img_byte_arr
