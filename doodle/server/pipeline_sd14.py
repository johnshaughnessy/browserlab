import torch
from diffusers import StableDiffusionImg2ImgPipeline
import gc

def init():
    pipe = StableDiffusionImg2ImgPipeline.from_pretrained("CompVis/stable-diffusion-v1-4", torch_dtype=torch.float16)
    pipe = pipe.to("cuda")
    return pipe

def img2img(pipe, prompt, input_image, strength, guidance_scale):
    return pipe(prompt=prompt, image=input_image, strength=strength, guidance_scale=guidance_scale).images[0]

def delete(pipe):
    del pipe
    gc.collect()
    torch.cuda.empty_cache()
