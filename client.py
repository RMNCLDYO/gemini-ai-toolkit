import json
import requests
from config import load_config
from loading import Loading

print("------------------------------------------------------------------\n")
print("                         Gemini AI Toolkit                        \n")     
print("               API Wrapper & Command-line Interface               \n")   
print("                       [v1.2.0] by @rmncldyo                      \n")  
print("------------------------------------------------------------------\n")

class Client:
    def __init__(self, api_key=None):
        self.config = load_config(api_key=api_key)
        self.api_key = api_key if api_key else self.config.get('api_key')
        self.base_url = self.config.get('base_url')
        self.version = self.config.get('version')
        self.timeout = self.config.get('timeout')
        self.headers = {
            "Content-Type": "application/json"
        }
    
    def get(self, endpoint):
        loading = Loading()
        url = f"{self.base_url}/{self.version}/{endpoint}?key={self.api_key}"
        try:
            loading.start()
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            response = response.json()
            return response
        except Exception as e:
            print(f"HTTP Error: {e}")
            raise
        finally:
            loading.stop()

    def post(self, endpoint, data):
        loading = Loading()
        url = f"{self.base_url}/{self.version}/{endpoint}?key={self.api_key}"
        try:
            loading.start()
            response = requests.post(url, json=data, headers=self.headers)
            response.raise_for_status()
            response = response.json()
            try:
                response["candidates"][0]["content"]["parts"][0]["text"]
                return response["candidates"][0]["content"]["parts"][0]["text"]
            except:
                try:
                    response["candidates"][0]["finishReason"]
                    if response["candidates"][0]["finishReason"] != "STOP":
                        if response["candidates"][0]["finishReason"] == "MAX_TOKENS":
                            reason = "The maximum number of tokens as specified in the request was reached."
                        elif response["candidates"][0]["finishReason"] == "SAFETY":
                            reason = "The content was flagged for safety reasons."
                        elif response["candidates"][0]["finishReason"] == "RECITATION":
                            reason = "The content was flagged for recitation reasons."
                        elif response["candidates"][0]["finishReason"] == "OTHER":
                            reason = "The content was flagged for unknown reasons."
                        return (f"[ WARNING ]: ({reason}) The response may be incomplete, but this is a normal behavior as set by Google's safety settings.")
                except:
                    return f"Error: {response}"
        except Exception as e:
            print(f"HTTP Error: {e}")
            raise
        finally:
            loading.stop()

    def stream_post(self, endpoint, data):
        loading = Loading()
        url = f"{self.base_url}/{self.version}/{endpoint}?key={self.api_key}"
        full_response = []
        response_content = ""
        buffer = ""
        try:
            loading.start()
            response = requests.post(url, json=data, headers=self.headers, stream=True)
            response.raise_for_status()
            loading.stop()
            print("Assistant: ", end="", flush=True)
            for chunk in response.iter_lines():
                chunk = chunk.decode("utf-8")
                chunk = chunk.strip()
                buffer += chunk
                try:
                    json_data = json.loads(buffer[1:])
                    if "candidates" in json_data and len(json_data["candidates"]) > 0:
                        candidate = json_data["candidates"][0]
                        if "content" in candidate and "parts" in candidate["content"] and len(candidate["content"]["parts"]) > 0:
                            response = candidate["content"]["parts"][0].get("text", "")
                            print(response, end="", flush=True)
                            response_content += response
                        elif candidate["finishReason"] != "STOP":
                            if candidate["finishReason"] == "MAX_TOKENS":
                                reason = "The maximum number of tokens as specified in the request was reached."
                            elif candidate["finishReason"] == "SAFETY":
                                reason = "The content was flagged for safety reasons."
                            elif candidate["finishReason"] == "RECITATION":
                                reason = "The content was flagged for recitation reasons."
                            elif candidate["finishReason"] == "OTHER":
                                reason = "The content was flagged for unknown reasons."
                            print(f"[ WARNING ]: ({reason}) The response may be incomplete, but this is a normal behavior as set by Google's safety settings.")
                        buffer = ""
                except json.JSONDecodeError:
                    pass
            full_response.append(response_content)
            print()
            return full_response[0]
        except Exception as e:
            print(f"Stream HTTP Error: {e}")
            raise
        finally:
            loading.stop()