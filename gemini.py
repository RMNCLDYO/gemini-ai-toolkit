import os
import time
import base64
import requests
from client import Client

class Chat:
    def __init__(self):
        self.client = None
        self.mode = "chat"
        self.folders = {}

    def run(self, api_key=None, model=None, prompt=None, stream=None, json=None, system_prompt=None, max_tokens=None, temperature=None, top_p=None, top_k=None, candidate_count=None, stop_sequences=None, safety_categories=None, safety_thresholds=None):
        
        self.client = Client(api_key=api_key)
        self.model = model if model else self.client.config.get('model')

        # Candidate count is not supported due to a bug in the API
        if candidate_count and candidate_count > 1:
            print("Error: Candidate count is not supported due to a bug in the API. Please use a candidate count of 1, or remove it completely.")
            exit(1)

        conversation_history = []
        
        print("Type 'exit' or 'quit' at any time to end the conversation.\n")
        
        print("Assistant: Hello! How can I assist you today?")
        while True:
            if prompt:
                user_input = prompt.strip()
                print(f"User: {user_input}")
                prompt = None
            else:
                user_input = input("User: ").strip()
                if user_input.lower() in ['exit', 'quit']:
                    print("\nThank you for using the Gemini AI toolkit. Have a great day!")
                    break

                if not user_input:
                    print("Error: Invalid input detected. Please enter a valid message.")
                    continue
            
            conversation_history.append({"role": "user", "parts": [{"text": user_input}]})

            conversation_data = {}

            if conversation_history:
                conversation_data["contents"] = conversation_history

            # System instructions are only supported in Gemini 1.5 Pro and later
            if system_prompt:
                if self.model == "gemini-1.5-pro-latest":
                    conversation_data["systemInstruction"] = {"parts": [{"text": system_prompt}]}
                else:
                    print("Error: System instructions are only supported in Gemini 1.5 Pro and later. Please use a model that supports system instructions.")
                    exit(1)

            # JSON mode is only supported in Gemini 1.5 Pro and later
            if json:
                if self.model == "gemini-1.5-pro-latest":
                    json_mode = "application/json"
                else:
                    print("Error: JSON mode is only supported in Gemini 1.5 Pro and later. Please use a model that supports JSON mode.")
                    exit(1)
            else:
                json_mode = None

            if safety_categories and safety_thresholds:
                if len(safety_categories) == len(safety_thresholds):
                    safety_data = []
                    for category, threshold in zip(safety_categories, safety_thresholds):
                        if SafetyValidator.validate(category, threshold):
                            safety_data.append({
                                "category": category,
                                "threshold": threshold
                            })
                        else:
                            error_message = ""
                            if category not in SafetyValidator.valid_categories:
                                if category in SafetyValidator.invalid_categories:
                                    error_message += f"Error: The safety category ('{category}') is not supported due to a bug in the API. "
                                else:
                                    error_message += f"Error: Invalid safety category ('{category}'). "
                            if threshold not in SafetyValidator.valid_thresholds:
                                error_message += f"Error: The safety threshold ('{threshold}') was not recognized."
                            if error_message:
                                print(f"Error: {error_message}")
                                exit(1)
                    
                    if safety_data:
                        conversation_data["safetySettings"] = safety_data
                else:
                    print("Error: If you are using safety settings, please make sure to provide both a safety category and a corresponding threshold. If you are providing multiple safety categories and thresholds, please make sure to provide them in the same order.")
                    exit(1)

            config_data = {
                "temperature": float(temperature) if temperature else None,
                "topP": float(top_p) if top_p else None,
                "topK": int(top_k) if top_k else None,
                "maxOutputTokens": int(max_tokens) if max_tokens else None,
                "candidateCount": int(candidate_count) if candidate_count else None, # Candidate count is not supported due to a bug in the API
                "stopSequences": stop_sequences if stop_sequences else None,
                "response_mime_type": json_mode if json_mode else None # JSON mode is only supported in Gemini 1.5 Pro and later
            }

            config_data = {k: v for k, v in config_data.items() if v is not None}

            if config_data:
                conversation_data["generationConfig"] = config_data

            data = conversation_data

            if stream:
                endpoint = f"models/{self.model}:streamGenerateContent"
                response = self.client.stream_post(endpoint, data, self.mode)
                assistant_response = response.strip()
            else:
                endpoint = f"models/{self.model}:generateContent"
                response = self.client.post(endpoint, data)
                assistant_response = response.strip()
                print(f"Assistant: {assistant_response}")
            conversation_history.append({"role": "model", "parts": [{"text": assistant_response}]})


class Text:
    def __init__(self):
        self.client = None
        self.mode = "text"

    def run(self, api_key=None, model=None, prompt=None, stream=None, json=None, system_prompt=None, max_tokens=None, temperature=None, top_p=None, top_k=None, candidate_count=None, stop_sequences=None, safety_categories=None, safety_thresholds=None):
        
        self.client = Client(api_key=api_key)
        self.model = model if model else self.client.config.get('model')

        if not prompt:
            print("Error: { Invalid input detected }. Please enter a valid message.")
            exit(1)

        # Candidate count is not supported due to a bug in the API
        if candidate_count and candidate_count > 1:
            print("Error: Candidate count is not supported due to a bug in the API. Please use a candidate count of 1, or remove it completely.")
            exit(1)
        
        conversation_data = {}

        prompt_data = {"role": "user", "parts": [{"text": prompt}]}
            
        if prompt_data:
            conversation_data["contents"] = [prompt_data]

        # System instructions are only supported in Gemini 1.5 Pro and later
        if system_prompt:
            if self.model == "gemini-1.5-pro-latest":
                conversation_data["systemInstruction"] = {"parts": [{"text": system_prompt}]}
            else:
                print("Error: System instructions are only supported in Gemini Pro 1.5 and later. Please use a model that supports system instructions.")
                exit(1)

        if safety_categories and safety_thresholds:
            if len(safety_categories) == len(safety_thresholds):
                safety_data = []
                for category, threshold in zip(safety_categories, safety_thresholds):
                    if SafetyValidator.validate(category, threshold):
                        safety_data.append({
                            "category": category,
                            "threshold": threshold
                        })
                    else:
                        error_message = ""
                        if category not in SafetyValidator.valid_categories:
                            if category in SafetyValidator.invalid_categories:
                                error_message += f"Error: The safety category ('{category}') is not supported due to a bug in the API. "
                            else:
                                error_message += f"Error: Invalid safety category ('{category}'). "
                        if threshold not in SafetyValidator.valid_thresholds:
                            error_message += f"Error: The safety threshold ('{threshold}') was not recognized."
                        if error_message:
                            print(f"Error: {error_message}")
                            exit(1)
                
                if safety_data:
                    conversation_data["safetySettings"] = safety_data
            else:
                print("Error: If you are using safety settings, please make sure to provide both a safety category and a corresponding threshold. If you are providing multiple safety categories and thresholds, please make sure to provide them in the same order.")
                exit(1)

        if json:
            if self.model == "gemini-1.5-pro-latest":
                json_mode = "application/json"
            else:
                print("Error: JSON mode is only supported in Gemini Pro 1.5 and later. Please use a model that supports JSON mode.")
                exit(1)
        else:
            json_mode = None

        config_data = {
            "temperature": float(temperature) if temperature else None,
            "topP": float(top_p) if top_p else None,
            "topK": int(top_k) if top_k else None,
            "maxOutputTokens": int(max_tokens) if max_tokens else None,
            "candidateCount": int(candidate_count) if candidate_count else None, # Candidate count is not supported due to a bug in the API
            "stopSequences": stop_sequences if stop_sequences else None,
            "response_mime_type": json_mode if json_mode else None # JSON mode is only supported in Gemini 1.5 Pro and later
        }

        config_data = {k: v for k, v in config_data.items() if v is not None}

        if config_data:
            conversation_data["generationConfig"] = config_data

        data = conversation_data

        if stream:
            endpoint = f"models/{self.model}:streamGenerateContent"
            response = self.client.stream_post(endpoint, data, self.mode)
            assistant_response = response.strip()
        else:
            endpoint = f"models/{self.model}:generateContent"
            response = self.client.post(endpoint, data)
            assistant_response = response.strip()
            print(f"Assistant: {assistant_response}")


class Vision:
    def __init__(self):
        self.client = None
        self.mode = "vision"
        self.folders = {}
        self.directory_path = os.path.dirname(__file__)
        self.image_folder_path = os.path.join(self.directory_path, 'images')
        os.makedirs(self.image_folder_path, exist_ok=True)

    def process_image_input(self, image_input):
        if image_input.startswith(('http://', 'https://', 'www')):
            image_path = self.download_image_and_save(image_input)
        elif os.path.exists(image_input):
            image_path = image_input
        else:
            image_path = None
            print(f"\nError: Image not found at path: {image_input}\n\nPlease check your image path or URL and try again.\n\n( If you are using a URL, please make sure the url starts with `http`, `https`, or `www`.)\n")
            exit()
        return image_path

    def download_image_and_save(self, image_url):
        response = requests.get(image_url)
        extension = self.get_mime_type(image_url).split("/")[1]
        if response.status_code == 200:
            filename = f"{str(time.time())}.{extension}"
            image_path = f"{self.image_folder_path}/{filename}"
            with open(image_path, 'wb') as f:
                f.write(response.content)
            return image_path
        else:
            print(f"Error: Failed to download image at url: {image_url}. Please check the URL and try again.")
            exit()
            
    def image_to_base64(self, image_path):
        try:
            with open(image_path, "rb") as image_file:
                return base64.b64encode(image_file.read()).decode('utf-8')
        except Exception as e:
            print(f"Error: Failed to convert the image to base64. Error: {e}")
            exit()
        
    def get_mime_type(self, image_path):
        if image_path.endswith((".jpg", ".jpeg")):
            return "image/jpeg"
        elif image_path.endswith(".png"):
            return "image/png"
        elif image_path.endswith(".webp"):
            return "image/webp"
        elif image_path.endswith(".heic"):
            return "image/heic"
        elif image_path.endswith(".heif"):
            return "image/heif"
        elif image_path.endswith(".pdf"):
            return "application/pdf"
        elif image_path.endswith(".mp4"):
            return "video/mp4"
        elif image_path.endswith(".mpeg"):
            return "video/mpeg"
        elif image_path.endswith(".mov"):
            return "video/mov"
        elif image_path.endswith(".avi"):
            return "video/avi"
        elif image_path.endswith(".flv"):
            return "video/x-flv"
        elif image_path.endswith(".mpg"):
            return "video/mpg"
        elif image_path.endswith(".webm"):
            return "video/webm"
        elif image_path.endswith(".wmv"):
            return "video/wmv"
        elif image_path.endswith(".3gp"):
            return "video/3gpp"
        elif image_path.endswith(".txt"):
            return "text/plain"
        elif image_path.endswith(".html"):
            return "text/html"
        elif image_path.endswith(".css"):
            return "text/css"
        elif image_path.endswith(".js"):
            return "text/javascript"
        elif image_path.endswith(".ts"):
            return "text/x-typescript"
        elif image_path.endswith(".csv"):
            return "text/csv"
        elif image_path.endswith(".md"):
            return "text/markdown"
        elif image_path.endswith(".py"):
            return "text/x-python"
        elif image_path.endswith(".json"):
            return "application/json"
        elif image_path.endswith(".xml"):
            return "text/xml"
        elif image_path.endswith(".rtf"):
            return "application/rtf"
        else:
            print(f"Error: Unsupported file format. Please use a supported file type including "
                  f".jpg, .jpeg, .png, .webp, .heic, .heif, .pdf, .mp4, .mpeg, .mov, .avi, .flv, "
                  f".mpg, .webm, .wmv, .3gp, .txt, .html, .css, .js, .ts, .csv, .md, .py, .json, "
                  f".xml, .rtf.")
            exit()


    def upload_image_file(self, image_path):
        endpoint = "upload/v1beta/files"
        url = f"{self.client.base_url}/{endpoint}?key={self.client.api_key}"
        
        with open(image_path, 'rb') as f:
            files = {
                'file': (os.path.basename(image_path), f, 'application/pdf')
            }
            response = requests.post(url, files=files)
        
        if response.status_code == 200:
            return response.json().get("file").get("uri")
        else:
            print(f"Error: Failed to upload file. Status code: {response.status_code}, Response: {response.text}")
            exit()

    def run(self, api_key=None, model=None, prompt=None, media=None, stream=None, json=None, system_prompt=None, max_tokens=None, temperature=None, top_p=None, top_k=None, candidate_count=None, stop_sequences=None, safety_categories=None, safety_thresholds=None):
        
        self.client = Client(api_key=api_key)
        self.model = model if model else self.client.config.get('model')
        if self.model != "gemini-pro-vision":
            self.model = "gemini-1.5-pro-latest"

        image_path = self.process_image_input(media)
        mime_type = self.get_mime_type(image_path)
        if mime_type == "application/pdf":
            print("Error: PDF files are not yet supported by Gemini's REST API.")
            exit(1)
            uploaded_file = self.upload_image_file(image_path)
        else:
            image_base64 = self.image_to_base64(image_path)

        # Candidate count is not supported due to a bug in the API
        if candidate_count and candidate_count > 1:
            print("Error: Candidate count is not supported due to a bug in the API. Please use a candidate count of 1, or remove it completely.")
            exit(1)

        conversation_data = {}

        prompt_data = {   
            "role": "user",
            "parts": []
        }

        if prompt:
            prompt_data["parts"].append({"text": prompt})

        if mime_type == "application/pdf":
            prompt_data["parts"].append({
                "fileData": {
                    "mimeType": mime_type,
                    "fileUri": uploaded_file
                }
            })
        else:
            prompt_data["parts"].append({
                "inlineData": {
                    "mimeType": mime_type,
                    "data": image_base64
                }
            })

        conversation_data = {"contents": prompt_data}

        # System instructions are only supported in Gemini Pro 1.5 and later
        if system_prompt:
            if self.model == "gemini-1.5-pro-latest":
                conversation_data["systemInstruction"] = {"parts": [{"text": system_prompt}]}
            else:
                print("Error: System instructions are only supported in Gemini Pro 1.5 and later. Please use a model that supports system instructions.")
                exit(1)

        # JSON mode is only supported in Gemini 1.5 Pro and later
        if json:
            if self.model == "gemini-1.5-pro-latest":
                json_mode = "application/json"
            else:
                print("Error: JSON mode is only supported in Gemini Pro 1.5 and later. Please use a model that supports JSON mode.")
                exit(1)
        else:
            json_mode = None

        if safety_categories and safety_thresholds:
            if len(safety_categories) == len(safety_thresholds):
                safety_data = []
                for category, threshold in zip(safety_categories, safety_thresholds):
                    if SafetyValidator.validate(category, threshold):
                        safety_data.append({
                            "category": category,
                            "threshold": threshold
                        })
                    else:
                        error_message = ""
                        if category not in SafetyValidator.valid_categories:
                            if category in SafetyValidator.invalid_categories:
                                error_message += f"Error: The safety category ('{category}') is not supported due to a bug in the API. "
                            else:
                                error_message += f"Error: Invalid safety category ('{category}'). "
                        if threshold not in SafetyValidator.valid_thresholds:
                            error_message += f"Error: The safety threshold ('{threshold}') was not recognized."
                        if error_message:
                            print(f"Error: {error_message}")
                            exit(1)
                
                if safety_data:
                    conversation_data["safetySettings"] = safety_data
            else:
                print("Error: If you are using safety settings, please make sure to provide both a safety category and a corresponding threshold. If you are providing multiple safety categories and thresholds, please make sure to provide them in the same order.")
                exit(1)

        config_data = {
            "temperature": float(temperature) if temperature else None,
            "topP": float(top_p) if top_p else None,
            "topK": int(top_k) if top_k else None,
            "maxOutputTokens": int(max_tokens) if max_tokens else None,
            "candidateCount": int(candidate_count) if candidate_count else None, # Candidate count is not supported due to a bug in the API
            "stopSequences": stop_sequences if stop_sequences else None,
            "response_mime_type": json_mode if json_mode else None # JSON mode is only supported in Gemini Pro 1.5 and later
        }

        config_data = {k: v for k, v in config_data.items() if v is not None}

        if config_data:
            conversation_data["generationConfig"] = config_data

        data = conversation_data

        if stream:
            endpoint = f"models/{self.model}:streamGenerateContent"
            response = self.client.stream_post(endpoint, data, self.mode)
            assistant_response = response.strip()
        else:
            endpoint = f"models/{self.model}:generateContent"
            response = self.client.post(endpoint, data)
            assistant_response = response.strip()
            print(f"Assistant: {assistant_response}")


class Audio:
    def __init__(self):
        self.client = None
        self.mode = "audio"
        self.folders = {}
        self.directory_path = os.path.dirname(__file__)
        self.audio_folder_path = os.path.join(self.directory_path, 'audio')
        os.makedirs(self.audio_folder_path, exist_ok=True)

    def process_audio_input(self, audio_input):
        if audio_input.startswith(('http://', 'https://', 'www')):
            audio_path = self.download_audio_file_and_save(audio_input)
        elif os.path.exists(audio_input):
            audio_path = audio_input
        else:
            audio_path = None
            print(f"\nError: Audio file not found at path: {audio_input}\n\nPlease check your audio path or URL and try again.\n\n( If you are using a URL, please make sure the url starts with `http`, `https`, or `www`.)\n")
            exit()
        return audio_path

    def download_audio_file_and_save(self, audio_url):
        response = requests.get(audio_url)
        extension = self.get_mime_type(audio_url).split("/")[1]
        if response.status_code == 200:
            filename = f"{str(time.time()).replace(".","_")}.{extension}"
            audio_path = f"{self.audio_folder_path}/{filename}"
            with open(audio_path, 'wb') as f:
                f.write(response.content)
            return audio_path
        else:
            print(f"Error: Failed to download audio at url: {audio_url}. Please check the URL and try again.")
            exit()
            
    def get_mime_type(self, audio_path):
        if audio_path.endswith(".wav"):
            return "audio/wav"
        elif audio_path.endswith(".mp3"):
            return "audio/mp3"
        elif audio_path.endswith(".aiff"):
            return "audio/aiff"
        elif audio_path.endswith(".aac"):
            return "audio/aac"
        elif audio_path.endswith(".ogg"):
            return "audio/ogg"
        elif audio_path.endswith(".flac"):
            return "audio/flac"
        else:
            print(f"Error: Unsupported audio format. Please use a .wav, .mp3, .aiff, .aac, .ogg, or .flac audio file.")
            exit()

    def upload_audio_file(self, audio_path):
        endpoint = "upload/v1beta/files"
        url = f"{self.client.base_url}/{endpoint}?key={self.client.api_key}"
        
        with open(audio_path, 'rb') as f:
            files = {
                'file': (os.path.basename(audio_path), f, 'audio/mp3')
            }
            response = requests.post(url, files=files)
        
        if response.status_code == 200:
            return response.json().get("file").get("uri")
        else:
            print(f"Error: Failed to upload file. Status code: {response.status_code}, Response: {response.text}")
            exit()


    def run(self, api_key=None, model=None, prompt=None, media=None, stream=None, json=None, system_prompt=None, max_tokens=None, temperature=None, top_p=None, top_k=None, candidate_count=None, stop_sequences=None, safety_categories=None, safety_thresholds=None):
        
        self.client = Client(api_key=api_key)
        self.model = model if model else self.client.config.get('model')

        # Audio mode is only supported in Gemini Pro 1.5 and later
        if "1.5" not in self.model:
            self.model = "gemini-1.5-pro-latest"

        # Candidate count is not supported due to a bug in the API
        if candidate_count and candidate_count > 1:
            print("Error: Candidate count is not supported due to a bug in the API. Please use a candidate count of 1, or remove it completely.")
            exit(1)

        conversation_data = {}

        prompt_data = {   
            "role": "user",
            "parts": []
        }

        if prompt:
            prompt_data["parts"].append({"text": prompt})

        if media:
            audio_path = self.process_audio_input(media)
            audio_uri = self.upload_audio_file(audio_path)
            mime_type = self.get_mime_type(audio_path)
            prompt_data["parts"].append({
                "fileData": {
                    "mimeType": mime_type,
                    "fileUri": audio_uri
                }
            })

        conversation_data = {"contents": prompt_data}

        # System instructions are only supported in Gemini Pro 1.5 and later
        if system_prompt:
            conversation_data["systemInstruction"] = {"parts": [{"text": system_prompt}]}
        else:
            system_prompt = None

        # JSON mode is only supported in Gemini Pro 1.5 and later
        if json:
            json_mode = "application/json"
        else:
            json_mode = None

        if safety_categories and safety_thresholds:
            if len(safety_categories) == len(safety_thresholds):
                safety_data = []
                for category, threshold in zip(safety_categories, safety_thresholds):
                    if SafetyValidator.validate(category, threshold):
                        safety_data.append({
                            "category": category,
                            "threshold": threshold
                        })
                    else:
                        error_message = ""
                        if category not in SafetyValidator.valid_categories:
                            if category in SafetyValidator.invalid_categories:
                                error_message += f"Error: The safety category ('{category}') is not supported due to a bug in the API. "
                            else:
                                error_message += f"Error: Invalid safety category ('{category}'). "
                        if threshold not in SafetyValidator.valid_thresholds:
                            error_message += f"Error: The safety threshold ('{threshold}') was not recognized."
                        if error_message:
                            print(f"Error: {error_message}")
                            exit(1)
                
                if safety_data:
                    conversation_data["safetySettings"] = safety_data
            else:
                print("Error: If you are using safety settings, please make sure to provide both a safety category and a corresponding safety threshold. If you are providing multiple safety categories and thresholds, please make sure to provide them in the same order.")
                exit(1)

        config_data = {
            "temperature": float(temperature) if temperature else None,
            "topP": float(top_p) if top_p else None,
            "topK": int(top_k) if top_k else None,
            "maxOutputTokens": int(max_tokens) if max_tokens else None,
            "candidateCount": int(candidate_count) if candidate_count else None, # Candidate count is not supported due to a bug in the API
            "stopSequences": stop_sequences if stop_sequences else None,
            "response_mime_type": json_mode if json_mode else None # JSON mode is only supported in Gemini Pro 1.5 and later
        }

        config_data = {k: v for k, v in config_data.items() if v is not None}

        if config_data:
            conversation_data["generationConfig"] = config_data

        data = conversation_data
        
        if stream:
            endpoint = f"models/{self.model}:streamGenerateContent"
            response = self.client.stream_post(endpoint, data, self.mode)
            assistant_response = response.strip()
        else:
            endpoint = f"models/{self.model}:generateContent"
            response = self.client.post(endpoint, data)
            assistant_response = response.strip()
            print(f"Assistant: {assistant_response}")


class SafetyValidator:
    invalid_categories = [
        'HARM_CATEGORY_UNSPECIFIED',
        'HARM_CATEGORY_DEROGATORY',
        'HARM_CATEGORY_TOXICITY',
        'HARM_CATEGORY_VIOLENCE',
        'HARM_CATEGORY_SEXUAL',
        'HARM_CATEGORY_MEDICAL',
        'HARM_CATEGORY_DANGEROUS'
    ]

    valid_categories = [
        # 'HARM_CATEGORY_UNSPECIFIED', # This category is not supported due to a bug in the API
        # 'HARM_CATEGORY_DEROGATORY', # This category is not supported due to a bug in the API
        # 'HARM_CATEGORY_TOXICITY', # This category is not supported due to a bug in the API
        # 'HARM_CATEGORY_VIOLENCE', # This category is not supported due to a bug in the API
        # 'HARM_CATEGORY_SEXUAL', # This category is not supported due to a bug in the API
        # 'HARM_CATEGORY_MEDICAL', # This category is not supported due to a bug in the API
        # 'HARM_CATEGORY_DANGEROUS', # This category is not supported due to a bug in the API
        'HARM_CATEGORY_HARASSMENT',
        'HARM_CATEGORY_HATE_SPEECH',
        'HARM_CATEGORY_SEXUALLY_EXPLICIT',
        'HARM_CATEGORY_DANGEROUS_CONTENT'
    ]

    valid_thresholds = [
        'HARM_BLOCK_THRESHOLD_UNSPECIFIED',
        'BLOCK_LOW_AND_ABOVE',
        'BLOCK_MEDIUM_AND_ABOVE',
        'BLOCK_ONLY_HIGH',
        'BLOCK_NONE'
    ]

    @classmethod
    def validate(cls, category, threshold):
        return category in cls.valid_categories and threshold in cls.valid_thresholds if category and threshold else False
    
    @classmethod
    def validate_categories(cls, category):
        return category in cls.invalid_categories if category else False
    
    @classmethod
    def validate_thresholds(cls, threshold):
        return threshold in cls.valid_thresholds if threshold else False
