import requests
import base64

class ImageGenerator:
    def __init__(self):
        return
    
    def save_image_to_file(self, image_description: str, file_path: str):
        payload = {
            "prompt": image_description,
            "steps": 20,
            "styles": ["High Quality HD"],
            "width": 768,
            "height": 768,
        }
        response = requests.post(url="http://127.0.0.1:7860/sdapi/v1/txt2img", json=payload)
        data = response.json()

        with open(file_path, 'wb') as file:
            file.write(base64.b64decode(data["images"][0]))
