import os
import requests
from dotenv import load_dotenv

load_dotenv()

class TextAPI:
    def __init__(self):
        self.api_key = os.getenv('API_KEY')
        if not self.api_key:
            raise ValueError("API key not found. Set the API_KEY environment variable.")

    def response(self, text_prompt: str) -> str:
        try:
            return self._response(text_prompt)
        except Exception as e:
            raise ValueError(f"Error generating caption: {e}")

    def _response(self, text_prompt: str) -> str:
        url = f"https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key={self.api_key}"
        headers = { "Content-Type": "application/json" }
        payload = {
            "contents": [
                {
                    "parts": [
                        { "text": text_prompt }
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