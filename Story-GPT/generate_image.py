import requests
import io
from PIL import Image
from dotenv import load_dotenv
import os

load_dotenv()
hf_api_key = os.getenv('HF_API_KEY')

# Hugging Face API details
API_URL = "https://api-inference.huggingface.co/models/merve/flux-lego-lora-dreambooth"
headers = {f"Authorization": f"Bearer {hf_api_key}"}

def generate_image(prompt):
    def query(payload):
        response = requests.post(API_URL, headers=headers, json=payload)
        if response.status_code == 200:
            return response.content
        else:
            print(f"Error: {response.status_code}, {response.text}")
            return None

    image_bytes = query({"inputs": prompt})
    if image_bytes:
        return Image.open(io.BytesIO(image_bytes))  # Return PIL Image object
    else:
        print(f"Failed to generate image for prompt: {prompt}")
        return None
