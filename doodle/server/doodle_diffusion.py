import torch
from PIL import Image
import io
import os
from diffusers import StableDiffusionImg2ImgPipeline
from diffusers import DiffusionPipeline, LCMScheduler


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
    print("Loaded the image!")
    images = pipe(prompt=prompt, image=init_image, strength=strength, guidance_scale=guidance_scale).images
    print("Processed the image!")
    processed_image = images[0];
    # Convert PIL Image back to byte data
    img_byte_arr = io.BytesIO()
    processed_image.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()
    return img_byte_arr

pixelart_pipe = None
def init_pipeline_pixelart():
    global pixelart_pipe
    model_id = "stabilityai/stable-diffusion-xl-base-1.0"
    lcm_lora_id = "latent-consistency/lcm-lora-sdxl"
    pixelart_pipe = DiffusionPipeline.from_pretrained(model_id, variant="fp16")
    pixelart_pipe.scheduler = LCMScheduler.from_config(pixelart_pipe.scheduler.config)

    pixelart_pipe.load_lora_weights(lcm_lora_id, adapter_name="lora")
    pixelart_pipe.load_lora_weights("./pixel-art-xl.safetensors", adapter_name="pixel")

    pixelart_pipe.set_adapters(["lora", "pixel"], adapter_weights=[1.0, 1.2])
    pixelart_pipe.to(device="cuda", dtype=torch.float16)


def process_image_pixelart(image_data, prompt, strength, guidance_scale):
    global pixelart_pipe
    negative_prompt = "3d render, realistic"

    img = pixelart_pipe(
        prompt=prompt,
        negative_prompt=negative_prompt,
        num_inference_steps=8,
        guidance_scale=1.5,
    ).images[0]

    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()
    return img_byte_arr
