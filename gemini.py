import os
import time
import base64
import requests
from client import Client

class Chat:
    def __init__(self):
        self.client = None

    def run(self, api_key=None, model=None, prompt=None, max_tokens=None, temperature=None, top_p=None, top_k=None, candidate_count=None, stop_sequences=None, safety_categories=None, safety_thresholds=None, stream=None):
        
        self.client = Client(api_key=api_key)
        self.model = model if model else self.client.config.get('model')

        # Candidate count is not supported due to a bug in the API
        if candidate_count and candidate_count > 1:
            print("Error: Candidate count is not supported due to a bug in the API. Please use a candidate count of 1, or remove it completely.")
            exit(1)

        conversation_history = []

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
                    print("Invalid input detected. Please enter a valid message.")
                    continue
            
            conversation_history.append({"role": "user", "parts": [{"text": user_input}]})

            conversation_data = {}

            if conversation_history:
                conversation_data["contents"] = conversation_history

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
                                print(error_message)
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
                "stopSequences": stop_sequences if stop_sequences else None
            }

            config_data = {k: v for k, v in config_data.items() if v is not None}

            if config_data:
                conversation_data["generationConfig"] = config_data

            data = conversation_data

            if stream:
                endpoint = f"models/{self.model}:streamGenerateContent"
                response = self.client.stream_post(endpoint, data)
                assistant_response = response
            else:
                endpoint = f"models/{self.model}:generateContent"
                response = self.client.post(endpoint, data)
                assistant_response = response
                print(f"Assistant: {assistant_response}")
            conversation_history.append({"role": "model", "parts": [{"text": assistant_response}]})


class Text:
    def __init__(self):
        self.client = None

    def run(self, api_key=None, model=None, prompt=None, temperature=None, top_p=None, top_k=None, max_tokens=None, candidate_count=None, stop_sequences=None, safety_categories=None, safety_thresholds=None, stream=None):
        
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
                            print(error_message)
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
            "stopSequences": stop_sequences if stop_sequences else None
        }

        config_data = {k: v for k, v in config_data.items() if v is not None}

        if config_data:
            conversation_data["generationConfig"] = config_data

        data = conversation_data

        if stream:
            endpoint = f"models/{self.model}:streamGenerateContent"
            response = self.client.stream_post(endpoint, data)
            assistant_response = response
        else:
            endpoint = f"models/{self.model}:generateContent"
            response = self.client.post(endpoint, data)
            assistant_response = response
            print(f"Assistant: {assistant_response}")


class Vision:
    def __init__(self):
        self.client = None
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
            print(f"\nImage not found at path: {image_input}\n\nPlease check your image path or URL and try again.\n\n( If you are using a URL, please make sure the url starts with `http`, `https`, or `www`.)\n")
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
            print(f"Failed to download image at url: {image_url}. Please check the URL and try again.")
            exit()
            
    def image_to_base64(self, image_path):
        try:
            with open(image_path, "rb") as image_file:
                return base64.b64encode(image_file.read()).decode('utf-8')
        except Exception as e:
            print(f"Failed to convert the image to base64. Error: {e}")
            exit()
        
    def get_mime_type(self, image_path):
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
            print(f"Unsupported image format. Please use a .jpg, .jpeg, .png, .webp, .heic, or .heif image file.")
            exit()

    def run(self, api_key=None, model=None, prompt=None, image=None, temperature=None, top_p=None, top_k=None, max_tokens=None, candidate_count=None, stop_sequences=None, safety_categories=None, safety_thresholds=None, stream=None):
        
        self.client = Client(api_key=api_key)
        self.model = model if model else self.client.config.get('model')
        if "vision" not in self.model:
            self.model = "gemini-pro-vision"

        image_path = self.process_image_input(image)
        image_base64 = self.image_to_base64(image_path)
        mime_type = self.get_mime_type(image_path)

        # Candidate count is not supported due to a bug in the API
        if candidate_count and candidate_count > 1:
            print("Error: Candidate count is not supported due to a bug in the API. Please use a candidate count of 1, or remove it completely.")
            exit(1)

        conversation_data = {}

        prompt_data = {   
            "role": "user",
            "parts":[
                {"text": prompt},
                {"inlineData": {"mimeType": mime_type, "data": image_base64}}
            ]
        }

        if prompt_data:
            conversation_data["contents"] = [prompt_data]

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
                            print(error_message)
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
            "stopSequences": stop_sequences if stop_sequences else None
        }

        config_data = {k: v for k, v in config_data.items() if v is not None}

        if config_data:
            conversation_data["generationConfig"] = config_data

        data = conversation_data
        
        if stream:
            endpoint = f"models/{self.model}:streamGenerateContent"
            response = self.client.stream_post(endpoint, data)
            assistant_response = response
        else:
            endpoint = f"models/{self.model}:generateContent"
            response = self.client.post(endpoint, data)
            assistant_response = response
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