import sys
import os
from client import Client
from validators import InputValidator, SafetyValidator
from file_handler import FileHandler

class GeminiBase:
    def __init__(self):
        self.client = None
        self.model = None
        self.input_validator = InputValidator()
        self.safety_validator = SafetyValidator()
        self.directory_path = os.path.dirname(__file__)
        self.file_handler = None

    def handle_user_input(self, user_input, mode):
        if user_input.lower() in ['exit', 'quit', '/exit', '/quit']:
            return "exit", None, None

        if user_input.lower() == '/clear':
            return "clear", None, None

        if mode == "multimodal" and user_input.startswith('/upload'):
            print()
            processed_files, user_text = self.file_handler.handle_upload_command(user_input)
            return "upload", processed_files, user_text

        return None, None, user_input

    def prepare_conversation_data(self, conversation_history, system_prompt, json, max_tokens, temperature, top_p, top_k, candidate_count, stop_sequences, safety_categories, safety_thresholds):
        conversation_data = {"contents": conversation_history}

        if system_prompt:
            conversation_data["systemInstruction"] = {'parts': [{'text': system_prompt}]}

        generation_config = {
            "temperature": float(temperature) if temperature else None,
            "topP": float(top_p) if top_p else None,
            "topK": int(top_k) if top_k else None,
            "maxOutputTokens": int(max_tokens) if max_tokens else None,
            "candidateCount": int(candidate_count) if candidate_count else None,
            "stopSequences": stop_sequences if stop_sequences else None,
        }
        if json:
            generation_config["responseMimeType"] = "application/json"
        
        generation_config = {k: v for k, v in generation_config.items() if v is not None}
        if generation_config:
            conversation_data["generationConfig"] = generation_config

        if safety_categories and safety_thresholds:
            safety_settings = []
            for category, threshold in zip(safety_categories, safety_thresholds):
                if self.safety_validator.validate(category, threshold):
                    safety_settings.append({"category": category, "threshold": threshold})
                else:
                    raise ValueError(f"Invalid safety setting: category '{category}', threshold '{threshold}'")
            if safety_settings:
                conversation_data["safetySettings"] = safety_settings

        return conversation_data
    
    def initialize_client(self, api_key, model):
        try:
            self.client = Client(api_key=api_key)
            self.model = model if model else self.client.config.get('model')
            self.file_handler = FileHandler(self.client.api_key, self.directory_path)
        except Exception as e:
            print(f"[ ERROR ]: Failed to initialize client: {str(e)}")
            sys.exit(1)