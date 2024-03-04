import base64
from loading import Loading
from base_api import BaseAPI

class VisionAPI(BaseAPI):
    def vision(self, image_path, vision_prompt):
        mime_type = self._mime_type(image_path)
        with open(image_path, "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode("utf-8")
        url = "https://generativelanguage.googleapis.com/v1/models/gemini-pro-vision:generateContent"
        payload = {
            "contents": [
                {
                    "parts": [
                        {"text": vision_prompt},
                        {"inlineData": {"mimeType": mime_type, "data": encoded_image}}
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

    def _mime_type(self, image_path):
        if image_path.endswith(".jpg") or image_path.endswith(".jpeg"):
            return "image/jpeg"
        elif image_path.endswith(".png"):
            return "image/png"
        elif image_path.endswith(".webp"):
            return "image/webp"
        elif image_path.endswith(".heic"):
            return "image/heic"
        elif image_path.endswith(".heif"):
            return "image/heif"
        else:
            raise ValueError("Unsupported image format.")
