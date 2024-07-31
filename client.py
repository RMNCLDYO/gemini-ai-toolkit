import sys
import json
import requests
from config import load_config
from loading import Loading

class Client:
    def __init__(self, api_key=None):
        try:
            self.config = load_config(api_key=api_key)
            self.api_key = api_key or self.config.get('api_key')
            self.base_url = self.config.get('base_url')
            self.model = self.config.get('model')
            self.version = self.config.get('version')
            self.headers = {"Content-Type": "application/json"}
            self.loading = Loading()
        except Exception as e:
            print(f"[ ERROR ]: Failed to initialize Client: {str(e)}")
            sys.exit(1)

    def get(self, endpoint=None, headers=None):
        try:
            response = self._make_request('GET', endpoint=endpoint, headers=headers)
            if response:
                return response.json()
            return None
        except Exception as e:
            print(f"[ ERROR ]: GET request failed: {str(e)}")
            return None

    def post(self, endpoint=None, data=None, headers=None):
        try:
            response = self._make_request('POST', endpoint=endpoint, data=data, headers=headers)
            if response:
                return self._handle_response(response.json())
            return None
        except Exception as e:
            print(f"[ ERROR ]: POST request failed: {str(e)}")
            return None

    def stream_post(self, endpoint=None, data=None, headers=None):
        try:
            response = self._make_request('POST', endpoint=endpoint, data=data, headers=headers, stream=True)
            if response:
                return self._handle_stream_response(response)
            return None
        except Exception as e:
            print(f"[ ERROR ]: Stream POST request failed: {str(e)}")
            return None
    
    def process_response(self, response=None, stream=None):
        if not stream and response:
            print(f"Assistant: {response.strip()}")
        return response
    
    def send_message(self, conversation_data=None, stream=None):
        try:
            endpoint = f"models/{self.model}:{'streamGenerateContent' if stream else 'generateContent'}"
            method = self.stream_post if stream else self.post
            return method(endpoint, conversation_data)
        except Exception as e:
            print(f"[ ERROR ]: Failed to send message: {str(e)}")
            return None

    def _make_request(self, method=None, endpoint=None, data=None, headers=None, stream=None):
        url = f"{self.base_url}/{self.version}/{endpoint}?key={self.api_key}"
        if stream:
            url += "&alt=sse"
        
        request_headers = self.headers
        if headers:
            request_headers = headers
        
        try:
            self.loading.start()
            response = requests.request(method=method, url=url, headers=request_headers, json=data, stream=stream, timeout=60)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            self._handle_request_errors(e)
            return None
        finally:
            self.loading.stop()

    def _handle_request_errors(self, error=None):
        if isinstance(error, requests.exceptions.HTTPError):
            status_code = error.response.status_code
            error_data = error.response.json().get('error', {})
            status = error_data.get('status')
            message = error_data.get('message', '')
            
            error_info = self._get_error_info(status_code, status, message)
            print(f"[ ERROR ]: {error_info}")
        elif isinstance(error, requests.exceptions.Timeout):
            print("[ ERROR ]: Request timed out. Please check your network connection and try again.")
        elif isinstance(error, requests.exceptions.ConnectionError):
            print("[ ERROR ]: Connection error. Please check your internet connection and try again.")
        else:
            print(f"[ ERROR ]: An unexpected error occurred: {str(error)}")
        
        return None

    def _get_error_info(self, status_code=None, status=None, message=None):
        error_map = {
            400: {
                "INVALID_ARGUMENT": "The request body is malformed. Check the API reference for request format, examples, and supported versions.",
                "FAILED_PRECONDITION": "Gemini API free tier is not available in your country. Please enable billing on your project in Google AI Studio."
            },
            403: {
                "PERMISSION_DENIED": "Your API key doesn't have the required permissions. Check that your API key is set and has the right access."
            },
            404: {
                "NOT_FOUND": "The requested resource wasn't found. Check if all parameters in your request are valid for your API version."
            },
            429: {
                "RESOURCE_EXHAUSTED": "You've exceeded the rate limit. Ensure you're within the model's rate limit. Request a quota increase if needed."
            },
            500: {
                "INTERNAL": "An unexpected error occurred on Google's side. Wait a bit and retry your request. If the issue persists, report it using the Send feedback button in Google AI Studio."
            },
            503: {
                "UNAVAILABLE": "The service may be temporarily overloaded or down. Wait a bit and retry your request. If the issue persists, report it using the Send feedback button in Google AI Studio."
            }
        }
        default_message = f"HTTP error occurred: {status_code} - {status}. {message}"
        return error_map.get(status_code, {}).get(status, default_message)
    
    def _handle_response(self, response_data=None):
        if "error" in response_data:
            error_message = response_data["error"].get("message", "Unknown API error")
            print(f"[ ERROR ]: API Error: {error_message}")
            return None

        candidates = response_data.get("candidates", [])
        if not candidates:
            print("[ ERROR ]: No response candidates received")
            return None

        candidate = candidates[0]
        finish_reason = candidate.get("finishReason")
        
        if finish_reason and finish_reason != "STOP":
            self._handle_safety_response(finish_reason)
            return ""

        content = candidate.get("content", {})
        parts = content.get("parts", [])
        if not parts:
            print("[ ERROR ]: No content parts in the response")
            return None

        return str(parts[0].get("text", "")).strip()

    def _handle_stream_response(self, response=None):
        response_content = ""
        print("Assistant: ", end="", flush=True)
        try:
            for line in response.iter_lines():
                if line:
                    line = line.decode('utf-8')
                    if line.startswith("data: "):
                        json_data = json.loads(line[6:])
                        chunk_text = (json_data.get("candidates", [{}])[0]
                                      .get("content", {})
                                      .get("parts", [{}])[0]
                                      .get("text", ""))
                        if chunk_text:
                            print(chunk_text, end="", flush=True)
                            response_content += chunk_text
            
            if response_content and not response_content.endswith("\n"):
                print()
        except json.JSONDecodeError:
            print("\n[ ERROR ]: Failed to decode JSON in stream response.")
        except Exception as e:
            print(f"\n[ ERROR ]: An error occurred while processing the stream: {str(e)}")
        
        return response_content

    def _handle_safety_response(self, finish_reason=None):
        reason_map = {
            "MAX_TOKENS": "The maximum number of tokens as specified in the request was reached.",
            "SAFETY": "The content was flagged for safety reasons.",
            "RECITATION": "The content was flagged for recitation reasons.",
            "OTHER": "The content was flagged for unknown reasons.",
            "BLOCKLIST": "The content contains forbidden terms.",
            "PROHIBITED_CONTENT": "The content potentially contains prohibited content.",
            "SPII": "The content potentially contains Sensitive Personally Identifiable Information (SPII).",
            "MALFORMED_FUNCTION_CALL": "The function call generated by the model is invalid."
        }
        reason = reason_map.get(finish_reason, "The response may be incomplete due to Google's safety settings.")
        print(f"\n[ WARNING ]: Generation stopped early. ({reason})")