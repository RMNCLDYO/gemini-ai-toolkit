import os
import requests
from dotenv import load_dotenv

load_dotenv()

class ChatAPI:
    def __init__(self):
        self.api_key = os.getenv('API_KEY')
        if not self.api_key:
            raise ValueError("API key not found. Set the API_KEY environment variable.")

    def update(self, chat_history: list) -> dict or None:
        try:
            return self._response(chat_history)
        except Exception as e:
            raise ValueError(f"Error generating chat response: {e}")

    def _response(self, chat_history: list) -> dict or None:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={self.api_key}"
        headers = {"Content-Type": "application/json"}
        payload = {"contents": chat_history}
        response = self._request(url, headers, payload)
        return response

    def response(self, chat_history: list) -> str or None:
        response = self.update(chat_history)
        if response and "candidates" in response and response["candidates"]:
            return response["candidates"][0]["content"]["parts"][0]["text"]
        return None

    def _request(self, url: str, headers: dict, payload: dict) -> dict:
        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise ValueError(f"Error communicating with Chat API: {e}")

