import base64
import requests
from PIL import Image
import io
import json

import modules.env as env

HOST=env.get("WEBUI_HOST")

def generate(prompt):
    payload = {
      "prompt": prompt,
      "negative_prompt": "EasyNegativeV2, (nsfw, nude:1.0)",
      "sampler_name": "UniPC",
      "steps": 30,
      "batch_size": 3,
      "cfg_scale": 7.5,
    }
    response = requests.post(url=f'http://{HOST}/sdapi/v1/txt2img', json=payload)

    r = response.json()

    images = []
    pnginfos = []
    for i, data in enumerate(r['images']):
        encoded = data.split(",",1)[0]
        image = Image.open(io.BytesIO(base64.b64decode(encoded)))
        images.append(image)

        pnginfo = json.loads(r['info'])['infotexts'][i].replace('Seed resize from: -1x-1, Denoising strength: 0, ', '')
        pnginfos.append(pnginfo)

    return images, pnginfos

async def loras():
    response = requests.get(url=f'http://{HOST}/sdapi/v1/loras')
    json = response.json()

    lora_names = list(map(lambda x: f"<lora:{x['alias']}:1>", json))

    return lora_names
