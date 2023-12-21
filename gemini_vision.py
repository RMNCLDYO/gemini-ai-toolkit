import os
import base64
import requests
from dotenv import load_dotenv

load_dotenv()

class VisionAPI:
    def __init__(self):
        self.api_key = os.getenv('API_KEY')
        if not self.api_key:
            raise ValueError("API key not found. Set the API_KEY environment variable.")

    def response(self, image_path: str, vision_prompt: str) -> str:
        try:
            with open(image_path, "rb") as image_file:
                image_data = image_file.read()
            mime_type = self._mime_type(image_path)
            encoded_image = base64.b64encode(image_data).decode("utf-8")
            return self._response(vision_prompt, encoded_image, mime_type)
        except Exception as e:
            raise ValueError(f"Error generating caption: {e}")

    def _mime_type(self, image_path: str) -> str:
        if image_path.endswith(".jpg"):
            return "image/jpeg"
        elif image_path.endswith(".png"):
            return "image/png"
        raise ValueError(f"Unsupported image format: {image_path}")

    def _response(self, vision_prompt: str, encoded_image: str, mime_type: str) -> str:
        url = f"https://generativelanguage.googleapis.com/v1/models/gemini-pro-vision:generateContent?key={self.api_key}"
        headers = { "Content-Type": "application/json" }
        payload = {
            "contents": [
                {
                    "parts": [
                        { "text": vision_prompt },
                        {
                            "inlineData": {
                                "mimeType": mime_type,
                                "data": encoded_image,
                            }
                        },
                    ]
                }
            ]
        }
        response = self._request(url, headers, payload)
        return response["candidates"][0]["content"]["parts"][0]["text"]

    def _request(self, url: str, headers: dict, payload: dict) -> dict:
        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise ValueError(f"Error communicating with API: {e}")