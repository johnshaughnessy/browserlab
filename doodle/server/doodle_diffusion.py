import torch
from PIL import Image
import io
from diffusers import StableDiffusionImg2ImgPipeline


pipe = None
def init_pipeline():
    global pipe
    # Initialize the pipeline
    model_id_or_path = "CompVis/stable-diffusion-v1-4"
    pipe = StableDiffusionImg2ImgPipeline.from_pretrained(model_id_or_path, torch_dtype=torch.float16)
    pipe = pipe.to("cuda")

def process_image_with_prompt(image_data, prompt, strength, guidance_scale):
    global pipe
    init_image = Image.open(io.BytesIO(image_data)).convert('RGB')
    images = pipe(prompt=prompt, image=init_image, strength=strength, guidance_scale=guidance_scale).images
    processed_image = images[0];
    # Convert PIL Image back to byte data
    img_byte_arr = io.BytesIO()
    processed_image.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()
    return img_byte_arr

