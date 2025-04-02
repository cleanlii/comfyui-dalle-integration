
import openai
import base64
import io
import os
import json
import torch
import asyncio
from PIL import Image
from torchvision.transforms import functional as TF

# 读取 API Key
NODE_FILE = os.path.abspath(__file__)
CONFIG_FILE = os.path.join(os.path.dirname(NODE_FILE), 'config.json')
def get_api_key() -> str:
    try:
        with open(CONFIG_FILE, "r") as f:
            config = json.load(f)
        return config["openAI_API_Key"]
    except:
        print("Error: config.json not found or invalid.")
        return ""

client = openai.AsyncOpenAI(api_key=get_api_key())

# ------------------- 图像生成节点 -------------------
class DalleImageGeneration:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {"multiline": True}),
                "size": (["1024x1024", "1024x1792", "1792x1024"],),
                "n": ("INT", {"default": 1, "min": 1, "max": 4}),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "generate"
    CATEGORY = "OpenAI/Dalle"

    def generate(self, prompt, size, n):
        async def fetch():
            try:
                response = await client.images.generate(
                    model="dall-e-3",
                    prompt=prompt,
                    size=size,
                    n=n,
                    response_format="b64_json"
                )
                return response
            except Exception as e:
                print(f"[Error] Generation failed: {e}")
                return None

        response = asyncio.run(fetch())
        if not response or not hasattr(response, "data"):
            return ([],)

        images = []
        for item in response.data:
            try:
                image = Image.open(io.BytesIO(base64.b64decode(item.b64_json))).convert("RGBA")
                tensor = TF.to_tensor(image)
                tensor[:3, tensor[3] == 0] = 0
                images.append(tensor)
            except Exception as e:
                print(f"[DecodeError] {e}")

        return (torch.stack(images).permute(0, 2, 3, 1),)

# ------------------- 图像编辑节点 -------------------
class DalleImageEdit:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "mask": ("IMAGE",),
                "prompt": ("STRING", {"multiline": True}),
                "size": (["1024x1024", "1024x1792", "1792x1024"],),
                "n": ("INT", {"default": 1, "min": 1, "max": 4}),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "edit"
    CATEGORY = "OpenAI/Dalle"

    def edit(self, image, mask, prompt, size, n):
        def tensor_to_pil(t):
            return TF.to_pil_image(t.permute(2, 0, 1).contiguous()).convert("RGBA")

        img_pil = tensor_to_pil(image[0])
        mask_pil = tensor_to_pil(mask[0]).resize(img_pil.size, Image.LANCZOS)

        # Resize both to target size
        size_map = {
            "1024x1024": (1024, 1024),
            "1024x1792": (1024, 1792),
            "1792x1024": (1792, 1024)
        }
        final_size = size_map.get(size, (1024, 1024))
        img_pil = img_pil.resize(final_size, Image.LANCZOS)
        mask_pil = mask_pil.resize(final_size, Image.LANCZOS)

        img_pil.save("/tmp/image_edit.png", "PNG")
        mask_pil.save("/tmp/mask_edit.png", "PNG")

        async def fetch():
            try:
                response = await client.images.edit(
                    image=open("/tmp/image_edit.png", "rb"),
                    mask=open("/tmp/mask_edit.png", "rb"),
                    prompt=prompt,
                    size=size,
                    n=n,
                    response_format="b64_json"
                )
                return response
            except Exception as e:
                print(f"[Error] Edit failed: {e}")
                return None

        response = asyncio.run(fetch())
        if not response or not hasattr(response, "data"):
            return ([],)

        images = []
        for item in response.data:
            try:
                image = Image.open(io.BytesIO(base64.b64decode(item.b64_json))).convert("RGBA")
                tensor = TF.to_tensor(image)
                tensor[:3, tensor[3] == 0] = 0
                images.append(tensor)
            except Exception as e:
                print(f"[DecodeError] {e}")

        return (torch.stack(images).permute(0, 2, 3, 1),)

# ------------------- 图像变体节点 -------------------
class DalleImageVariation:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "size": (["1024x1024", "1024x1792", "1792x1024"],),
                "n": ("INT", {"default": 1, "min": 1, "max": 4}),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "variant"
    CATEGORY = "OpenAI/Dalle"

    def variant(self, image, size, n):
        def tensor_to_pil(t):
            return TF.to_pil_image(t.permute(2, 0, 1).contiguous()).convert("RGBA")

        img_pil = tensor_to_pil(image[0])
        size_map = {
            "1024x1024": (1024, 1024),
            "1024x1792": (1024, 1792),
            "1792x1024": (1792, 1024)
        }
        img_pil = img_pil.resize(size_map.get(size, (1024, 1024)), Image.LANCZOS)
        img_pil.save("/tmp/variant_image.png", "PNG")

        async def fetch():
            try:
                response = await client.images.create_variation(
                    image=open("/tmp/variant_image.png", "rb"),
                    size=size,
                    n=n,
                    response_format="b64_json"
                )
                return response
            except Exception as e:
                print(f"[Error] Variation failed: {e}")
                return None

        response = asyncio.run(fetch())
        if not response or not hasattr(response, "data"):
            return ([],)

        images = []
        for item in response.data:
            try:
                image = Image.open(io.BytesIO(base64.b64decode(item.b64_json))).convert("RGBA")
                tensor = TF.to_tensor(image)
                tensor[:3, tensor[3] == 0] = 0
                images.append(tensor)
            except Exception as e:
                print(f"[DecodeError] {e}")

        return (torch.stack(images).permute(0, 2, 3, 1),)

# 注册节点
NODE_CLASS_MAPPINGS = {
    "DalleImageGeneration": DalleImageGeneration,
    "DalleImageEdit": DalleImageEdit,
    "DalleImageVariation": DalleImageVariation,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "DalleImageGeneration": "Dalle Image Generation",
    "DalleImageEdit": "Dalle Image Edit",
    "DalleImageVariation": "Dalle Image Variation",
}
