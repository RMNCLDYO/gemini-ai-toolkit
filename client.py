import json
import time
import requests
from config import load_config
from loading import Loading

print("------------------------------------------------------------------\n")
print("                         Gemini AI Toolkit                        \n")     
print("               API Wrapper & Command-line Interface               \n")   
print("                       [v1.2.1] by @rmncldyo                      \n")  
print("------------------------------------------------------------------\n")

class Client:
    def __init__(self, api_key=None):
        self.config = load_config(api_key=api_key)
        self.api_key = api_key if api_key else self.config.get('api_key')
        self.base_url = self.config.get('base_url')
        self.model = self.config.get('model')
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
            response = response.json()
            try:
                response["error"]
                loading.stop()
                if response["error"]["message"] == "Resource has been exhausted (e.g. check quota).":
                    print(f"[ ERROR ]: Rate limit exceeded. Sleeping for 15 seconds while we cool down. One moment please...")
                    time.sleep(15)
                    return "Slept for a few seconds, go ahead and try again now that we have allowed the model to cool down."
                else:
                    print(f"[ ERROR ]: {response['error']['message']}")
                    exit(1)
            except:
                pass
            try:
                response["candidates"][0]["content"]["parts"][0]["text"]
                return response["candidates"][0]["content"]["parts"][0]["text"]
            except:
                try:
                    response["candidates"][0]["finishReason"]
                    if response["candidates"][0]["finishReason"] != "STOP":
                        reason_map = {
                            "MAX_TOKENS": "The maximum number of tokens as specified in the request was reached.",
                            "SAFETY": "The content was flagged for safety reasons.",
                            "RECITATION": "The content was flagged for recitation reasons.",
                            "OTHER": "The content was flagged for unknown reasons."
                        }
                        reason = reason_map.get(response["candidates"][0]["finishReason"], "The response may be incomplete, but this is a normal behavior as set by Google's safety settings.")
                        print(f"\n[ WARNING ]: ({reason})")
                except json.JSONDecodeError:
                    pass
                except KeyError:
                    print("\nError processing the response.")
                except Exception as e:
                    return f"Error: {e}"
        except Exception as e:
            print(f"HTTP Error: {e}")
            raise
        finally:
            loading.stop()

    def stream_post(self, endpoint, data, mode):
        loading = Loading()
        url = f"{self.base_url}/{self.version}/{endpoint}?key={self.api_key}"
        full_response = []
        response_content = ""
        buffer = ""
        try:
            loading.start()
            response = requests.post(url, json=data, headers=self.headers, stream=True)
            loading.stop()
            print("Assistant: ", end="", flush=True)
            for chunk in response.iter_lines():
                chunk = chunk.decode("utf-8")
                chunk = chunk.strip()
                buffer += chunk
                try:
                    json_data = json.loads(buffer[1:])
                    try:
                        json_data["error"]
                        if json_data["error"]["message"] == "Resource has been exhausted (e.g. check quota).":
                            print(f"[ ERROR ]: Rate limit exceeded. Sleeping for 15 seconds while we cool down. One moment please...")
                            time.sleep(15)
                            return "Slept for a few seconds, go ahead and try again now that we have allowed the model to cool down."
                        else:
                            print(f"[ ERROR ]: {json_data['error']['message']}")
                            exit(1)
                    except:
                        pass
                    if "candidates" in json_data and len(json_data["candidates"]) > 0:
                        candidate = json_data["candidates"][0]
                        if "content" in candidate and "parts" in candidate["content"] and len(candidate["content"]["parts"]) > 0:
                            response = candidate["content"]["parts"][0].get("text", "")
                            is_final = candidate.get("finishReason")
                            if is_final == "STOP":
                                if mode == "chat":
                                    print(response.strip(), end="")
                                else:
                                    print(response, end="", flush=True)
                            else:
                                print(response, end="", flush=True)
                            response_content += response
                        elif candidate.get("finishReason") != "STOP":
                            reason_map = {
                                "MAX_TOKENS": "The maximum number of tokens as specified in the request was reached.",
                                "SAFETY": "The content was flagged for safety reasons.",
                                "RECITATION": "The content was flagged for recitation reasons.",
                                "OTHER": "The content was flagged for unknown reasons."
                            }
                            reason = reason_map.get(candidate.get("finishReason"), "The response may be incomplete, but this is a normal behavior as set by Google's safety settings.")
                            print(f"\n[ WARNING ]: ({reason})")
                        buffer = ""
                except json.JSONDecodeError:
                    pass
                except KeyError:
                    print("\nError processing the response.")
                    break
            full_response.append(response_content)
            # The Gemini Pro 1.5 model has a different streaming response format, adding a newline to separate responses in models previous to 1.5.
            if self.model != "gemini-pro-1.5-latest":
                print()
            return full_response[0]
        except Exception as e:
            print(f"Stream HTTP Error: {e}")
            raise
        finally:
            loading.stop()