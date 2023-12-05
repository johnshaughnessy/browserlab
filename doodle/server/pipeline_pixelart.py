from diffusers import StableDiffusionXLImg2ImgPipeline, LCMScheduler
import torch
import gc

def init():
    pipe = StableDiffusionXLImg2ImgPipeline.from_pretrained(
        "stabilityai/stable-diffusion-xl-base-1.0", torch_dtype=torch.float16, variant="fp16", use_safetensors=True
    ).to("cuda")
    pipe.scheduler = LCMScheduler.from_config(pipe.scheduler.config)
    pipe.load_lora_weights("latent-consistency/lcm-lora-sdxl", adapter_name="lora")
    pipe.load_lora_weights("nerijs/pixel-art-xl", adapter_name="pixel")
    pipe.set_adapters(["lora", "pixel"], adapter_weights=[1.0, 1.0])
    pipe.to(device="cuda", dtype=torch.float16)
    return pipe

def delete(pipe):
    del pipe
    gc.collect()
    torch.cuda.empty_cache()

def img2img(pipe, prompt, input_image, strength, guidance_scale):
    return pipe(prompt, image=input_image, num_inference_steps=20, strength=strength, guidance_scale=guidance_scale).images[0]
