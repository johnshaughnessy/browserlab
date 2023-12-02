import torch
from PIL import Image
import io
import os
from diffusers import StableDiffusionXLImg2ImgPipeline
from diffusers import DiffusionPipeline, LCMScheduler


# pipe = None
# def init_pipeline():
#     global pipe
#     # Initialize the pipeline
#     model_id_or_path = "CompVis/stable-diffusion-v1-4"
#     pipe = StableDiffusionImg2ImgPipeline.from_pretrained(model_id_or_path, torch_dtype=torch.float16)
#     pipe = pipe.to("cuda")

# def process_image_with_prompt(image_data, prompt, strength, guidance_scale):
#     global pipe
#     init_image = Image.open(io.BytesIO(image_data)).convert('RGB')
#     images = pipe(prompt=prompt, image=init_image, strength=strength, guidance_scale=guidance_scale).images
#     processed_image = images[0];
#     # Convert PIL Image back to byte data
#     img_byte_arr = io.BytesIO()
#     processed_image.save(img_byte_arr, format='PNG')
#     img_byte_arr = img_byte_arr.getvalue()
#     return img_byte_arr

pixelart_pipe = None
def init_pipeline_pixelart():
    global pixelart_pipe
    # pixelart_pipe = DiffusionPipeline.from_pretrained(model_id, variant="fp16")
    pixelart_pipe = StableDiffusionXLImg2ImgPipeline.from_pretrained("stabilityai/stable-diffusion-xl-base-1.0", variant="fp16")
    #pixelart_pipe.scheduler = LCMScheduler.from_config(pixelart_pipe.scheduler.config)

    #pixelart_pipe.load_lora_weights("latent-consistency/lcm-lora-sdxl", adapter_name="lora")
    #pixelart_pipe.load_lora_weights("nerijs/pixel-art-xl", adapter_name="pixel")
    #pixelart_pipe.set_adapters(["lora", "pixel"], adapter_weights=[1.0, 1.2])
    pixelart_pipe.to(device="cuda", dtype=torch.float16)


def process_image_pixelart(image_data, prompt, strength, guidance_scale):


    global pixelart_pipe
    negative_prompt = "3d render, realistic"
    init_image = Image.open(io.BytesIO(image_data)).convert('RGB')
    print("Image size:")
    print(init_image.size)
    #init_image = init_image.resize((1024, 1024))
    #print("Image size:")
    #print(init_image.size)
    # Convert to

    img = pixelart_pipe(
        prompt=prompt,
        negative_prompt=negative_prompt,
        image=init_image,
        strength=strength,
        guidance_scale=1.5,
#        num_inference_steps=8,
    ).images[0]

    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()
    return img_byte_arr


from diffusers import DiffusionPipeline
import torch

def init_pipeline():
    global base
    global refiner
    # load both base & refiner
    base = DiffusionPipeline.from_pretrained(
        "stabilityai/stable-diffusion-xl-base-1.0", torch_dtype=torch.float16, variant="fp16", use_safetensors=True
       )
    base.to("cuda")
    refiner = DiffusionPipeline.from_pretrained(
        "stabilityai/stable-diffusion-xl-refiner-1.0",
        text_encoder_2=base.text_encoder_2,
        vae=base.vae,
        torch_dtype=torch.float16,
        use_safetensors=True,
        variant="fp16",
       )
    refiner.to("cuda")

def process_image_with_prompt(image_data, prompt, strength, guidance_scale):
    global base
    global refiner

    # Define how many steps and what % of steps to be run on each experts (80/20) here
    n_steps = 40
    high_noise_frac = 0.8

    prompt = "A majestic lion jumping from a big stone at night"

    # run both experts
    image = base(
        prompt=prompt,
        num_inference_steps=n_steps,
        denoising_end=high_noise_frac,
        output_type="latent",
       ).images
    #image = refiner(
    #    prompt=prompt,
    #    num_inference_steps=n_steps,
    #    denoising_start=high_noise_frac,
    #    image=image,
    #   ).images[0]

    # If the image tensor is of shape [1, C, H, W], remove the batch dimension
    if image.dim() == 4 and image.shape[0] == 1:
        print("Removing batch dimension")
        image = image.squeeze(0)  # Remove batch dimension
    else:
        print("Image shape: " + str(image.shape))

    # Convert the tensor to a PIL Image
    # Assuming the tensor is normalized in the range [-1, 1]
    image = (image + 1) / 2
    image = image.clamp(0, 1)
    image = image.permute(1, 2, 0)  # Change from CxHxW to HxWxC
    image = image.cpu().numpy()
    image = (image * 255).astype('uint8')
    image = Image.fromarray(image)

    # Convert PIL Image back to byte data
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()
    return img_byte_arr
