from loading import Loading
from base_api import BaseAPI

class TextAPI(BaseAPI):
    def text(self, text_prompt):
        url = "https://generativelanguage.googleapis.com/v1/models/gemini-1.0-pro-latest:generateContent"
        payload = {
            "contents": [
                {
                    "parts": [
                        {"text": text_prompt}
                    ]
                }
            ]
        }
        loading = Loading()
        loading.start()

        try:
            response = self.post(f"{url}?key={self.api_key}", payload)
        finally:
            loading.stop()

        if response and "candidates" in response and response["candidates"]:
            print(response["candidates"][0]["content"]["parts"][0]["text"])
        else:
            print("No response or error occurred.")